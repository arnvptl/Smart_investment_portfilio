import pandas as pd
import numpy as np
from calculation import simple_return, max_sharp_portfolio, portfolio_with_target_risk, generate_random_weights, portfilio_performence
from plotter import plot_efficient_frontier

def optimize_for_user(stock_data, risk_free_rate=0.0, risk=None, show_plot=False):
    returns = simple_return(stock_data)

    # 🎯 Optimization logic
    if not risk:
        result = max_sharp_portfolio(returns, risk_free_rate)
    else:
        result = portfolio_with_target_risk(returns, risk_free_rate, risk)

    # 📊 If user wants plot, generate frontier values
    if show_plot:
        risks_list = []
        returns_list = []
        sharpe_list = []

        for _ in range(5000):  # Random portfolio simulation
            weights = generate_random_weights(len(returns.columns))
            exp_return, risk, sharpe = portfilio_performence(weights, returns)
            returns_list.append(exp_return)
            risks_list.append(risk)
            sharpe_list.append(sharpe)

        plot_efficient_frontier(returns_list, risks_list, sharpe_list, result)

    return result


if __name__=='__main__':
    from data_featch import data_featch

    tickers = ["AAPL", "MSFT", "GOOGL"]
    data = data_featch(tickers,1)
    result = optimize_for_user(data,risk_free_rate=0.0,risk_tolerance=0.33,show_plot=True)
    if result['Optimal Weights'] is not None:
        print("\n📊 Portfolio Optimization Result\n")
        print("Ticker\t\tWeight")
        print("--------------------------------")
        for ticker, weight in zip(tickers, result['Optimal Weights']):
            print(f"{ticker}\t\t{weight:.4f}")
            print("\nExpected Return   :", round(result['Expected Return'], 4))
            print("Risk (Volatility) :", round(result['Risk (Volatility)'], 4))
            print("Sharpe Ratio      :", round(result['Sharpe Ratio'], 4))
            print("\n")
    else:
        print("⚠ Optimization Failed. Please check data or internet connection.")


