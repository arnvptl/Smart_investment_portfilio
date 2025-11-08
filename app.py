from flask import Flask, request, render_template
from portfolio.data_featch import get_data
from portfolio.calculation import simple_return
from portfolio.calculation import max_sharp_portfolio, portfolio_with_target_risk
import os
import matplotlib.pyplot as plt

STOCK_NAMES = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "INFY.NS": "Infosys",
    "HDFCBANK.NS": "HDFC Bank",
    "ICICIBANK.NS": "ICICI Bank",
    "SBIN.NS": "State Bank of India",
    "ITC.NS": "ITC Limited",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "BAJFINANCE.NS": "Bajaj Finance",
    "LT.NS": "Larsen & Toubro",
    "BHARTIARTL.NS": "Bharti Airtel",
    "ASIANPAINT.NS": "Asian Paints",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "MARUTI.NS": "Maruti Suzuki",
    "TITAN.NS": "Titan Company"
}

app = Flask(__name__)

def format_indian_currency(amount):
    """Format currency in Indian style with Crores and Lakhs"""
    if amount >= 10000000:
        return f"₹{amount / 10000000:.2f} Cr"
    elif amount >= 100000:
        return f"₹{amount / 100000:.2f} L"
    else:
        return f"₹{amount:,.2f}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=['POST'])
def submit():
    tickers = request.form.getlist('symbols')
    amount = float(request.form['amount'])
    risk = float(request.form['risk']) / 100
    years = float(request.form['years'])

    # Fetch stock price data
    stock_data = get_data(tickers, years)
    returns = simple_return(stock_data)

    # Determine which model to run
    if risk == 0:
        result = max_sharp_portfolio(returns)
        
    else:
        result = portfolio_with_target_risk(returns, risk)


    weights = result["Optimal Weights"]
    expected_return = result["Expected Return"]

    expected_profit_money = expected_return * amount * years
    final_portfolio_value = amount + expected_profit_money

    #------------------Plot Section-------------------#
    plot_dir = os.path.join("static", "plots")
    os.makedirs(plot_dir, exist_ok=True)
    plt.style.use('dark_background')

    custom_colors = [
        '#7C4DFF', '#536DFE', '#448AFF', '#00BCD4', '#4CAF50',
        '#FFC107', '#FF7043', '#E91E63', '#9C27B0', '#2196F3'
    ]

    # ----- PIE CHART -----
    plt.figure(figsize=(6, 6), facecolor='#0B0C2A')
    wedges, texts, autotexts = plt.pie(
        weights,
        labels=[STOCK_NAMES.get(symbol, symbol) for symbol in tickers],
        autopct='%1.1f%%',
        startangle=140,
        colors=custom_colors,
        wedgeprops={'edgecolor': '#0B0C2A', 'linewidth': 1.5}
    )
    for text in texts: text.set_color('#E0E0E0')
    for autotext in autotexts:
        autotext.set_color('#FFFFFF')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    plt.title("Portfolio Allocation by Stock", fontsize=14, color='#B388FF', pad=20)
    plt.tight_layout()
    pie_path = os.path.join(plot_dir, "allocation.png")
    plt.savefig(pie_path, bbox_inches='tight', facecolor='#0B0C2A', dpi=300)
    plt.close()

    # ----- SCATTER PLOT -----
    plt.figure(figsize=(6, 4), facecolor='#0B0C2A')
    plt.scatter(
        result["Risk (Volatility)"] * 100,
        result["Expected Return"] * 100,
        color='#FF4081', s=120, edgecolors='white', linewidth=1.2, label="Your Portfolio"
    )
    plt.title("Risk vs Expected Return", fontsize=13, color='#B388FF', pad=15)
    plt.xlabel("Risk (Volatility) %", color='#B0BEC5', fontsize=11)
    plt.ylabel("Expected Return %", color='#B0BEC5', fontsize=11)
    plt.grid(True, linestyle='--', alpha=0.3, color='#757575')
    plt.legend(facecolor='#1A1B3A', edgecolor='none', labelcolor='white', fontsize=10)
    plt.tight_layout()
    scatter_path = os.path.join(plot_dir, "risk_return.png")
    plt.savefig(scatter_path, bbox_inches='tight', facecolor='#0B0C2A', dpi=300)
    plt.close()

    # ----- BAR CHART (Weight Distribution) -----
    plt.figure(figsize=(8, 5), facecolor='#0B0C2A')
    plt.bar(
        [STOCK_NAMES.get(symbol, symbol) for symbol in tickers],
        [w * 100 for w in weights],
        color=custom_colors[:len(tickers)],
        edgecolor='white'
    )
    plt.title("Weight Distribution (%)", fontsize=13, color='#B388FF', pad=15)
    plt.ylabel("Weight %", color='#B0BEC5')
    plt.xticks(rotation=45, ha='right', color='#E0E0E0', fontsize=9)
    plt.yticks(color='#E0E0E0')
    plt.tight_layout()
    bar_path = os.path.join(plot_dir, "weight_distribution.png")
    plt.savefig(bar_path, bbox_inches='tight', facecolor='#0B0C2A', dpi=300)
    plt.close()

    # --------- Format all output nicely ----------
    formatted_data = {
        "risk": f"{risk*100:.0f}%",
        "investment": format_indian_currency(amount),
        "expected_return_percent": f"{expected_return * 100:.2f}% per year",
        "expected_profit_money": format_indian_currency(expected_profit_money),
        "final_value": format_indian_currency(final_portfolio_value),
        "risk_percent": f"{result['Risk (Volatility)'] * 100:.2f}%",
        "sharpe_ratio": f"{result['Sharpe Ratio']:.2f}",
        "weights": [f"{w * 100:.2f}%" for w in weights],
        "allocated": [format_indian_currency(w * amount) for w in weights],
        "symbols": [STOCK_NAMES.get(symbol, symbol) for symbol in tickers],
        "years": int(years),
        "pie_chart": "/" + pie_path.replace("\\", "/"),
        "scatter_chart": "/" + scatter_path.replace("\\", "/"),
        "bar_chart": "/" + bar_path.replace("\\", "/"),
        "message": result["Message"]
    }

    return render_template("result.html", data=formatted_data)

if __name__ == '__main__':
    app.run(debug=True)
