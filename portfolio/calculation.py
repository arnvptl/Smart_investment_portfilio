import pandas as pd
import numpy as np

def simple_return(df):
    """
        Calulate the daily return of the stock prise
    """
    returns = df.pct_change().dropna()
    return returns

def portfilio_performence(weights,returns,risk_free_rate=0.0):
    """
    Calculate portfolio performance: expected return, volatility, and Sharpe Ratio.
    
    weights: list/array of asset weights
    returns: daily returns dataframe
    risk_free_rate: annual risk-free rate

    expected_return : u_p = wT * u *252 //Annula return

    """
    weights = np.array(weights)
    mean_daily_returns = returns.mean()
    # Expected portfolio return
    expected_return = np.dot(weights, mean_daily_returns) * 252

    # Portfolio variance and standard deviation (volatility/risk)
    cov_matrix = returns.cov() *252 # Annulized
    portfolio_volatility = np.sqrt(np.dot(weights.T,np.dot(cov_matrix,weights)))

    # Sharpe Ratio
    sharpe_ratio = (expected_return - risk_free_rate) / portfolio_volatility

    return expected_return,portfolio_volatility,sharpe_ratio


def generate_random_weights(num_assets):
    """
    Generate random portfolio weights that sum to 1.

    """
    weights = np.random.random(num_assets)
    weights/=sum(weights)
    return weights

def max_sharp_portfolio(returns, risk_free_rate=0.0, num_portfolios=5000):
    """
    Generate multiple random portfolios and return the one with the highest Sharpe Ratio.
    """
    num_assets = len(returns.columns)

    best_sharp = -999
    best_weight = None
    best_return = None
    best_risk = None

    for _ in range(num_portfolios):
        weights = generate_random_weights(num_assets)
        exp_return,risk,sharp = portfilio_performence(weights,returns,risk_free_rate)


        if sharp > best_sharp:
            best_sharp = sharp
            best_weight = weights
            best_return = exp_return
            best_risk = risk
    
    return {
        "Optimal Weights": best_weight,
        "Expected Return": best_return,
        "Risk (Volatility)": best_risk,
        "Sharpe Ratio": best_sharp,
        "Message" : "⚠️ Your chosen risk level could not be achieved. Showing the best risk-adjusted portfolio (Maximum Sharpe Ratio)."
    }

def portfolio_with_target_risk(returns, target_risk, risk_free_rate=0.0, num_portfolios=5000, tolerance=0.1):
    """
    Find a portfolio whose risk (volatility) is as close as possible to the target risk.

    returns      : Daily returns of all selected stocks
    target_risk  : The risk (volatility) value user wants (annualized)
    tolerance    : Allowed difference between portfolio risk & target risk
    """
    num_assets = len(returns.columns)

    best_diff = float('inf')
    best_weight = None
    best_return = None
    best_risk = None
    best_sharpe = None

    for _ in range(num_portfolios):
        weights = generate_random_weights(num_assets)
        exp_return, risk, sharpe = portfilio_performence(weights, returns, risk_free_rate)

        # Check how close this risk is to target risk
        risk_diff = abs(risk - target_risk)

        if risk_diff < best_diff and risk_diff <= tolerance:
            best_diff = risk_diff
            best_weight = weights
            best_return = exp_return
            best_risk = risk
            best_sharpe = sharpe
    if best_weight is None:
        return max_sharp_portfolio(returns)
    
    return {
        "Optimal Weights": best_weight,
        "Expected Return": best_return,
        "Risk (Volatility)": best_risk,
        "Sharpe Ratio": best_sharpe,
        "Message": "✅ Portfolio optimized successfully for your chosen risk level."
    }



