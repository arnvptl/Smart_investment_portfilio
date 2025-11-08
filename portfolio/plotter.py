import numpy as np
import matplotlib.pyplot as plt

def plot_efficient_frontier(portfolio_returns, portfolio_risks, sharpe_ratios,
                            max_sharpe_portfolio=None):
    """
    Plots:
    - Efficient Frontier (Risk vs. Expected Return)
    - Scatter of random portfolios
    - Highlights the Maximum Sharpe Ratio Portfolio (if available)

    Parameters:
    - portfolio_returns: List/array of expected returns of portfolios
    - portfolio_risks: List/array of risks (volatility/std dev)
    - sharpe_ratios: List/array of sharpe ratios of each portfolio
    - max_sharpe_portfolio: Dict containing details of best Sharpe portfolio:
        {
           "Optimal Weights": [...],
           "Expected Return": ...,
           "Risk (Volatility)": ...,
           "Sharpe Ratio": ...
        }
    """

    plt.figure(figsize=(10, 6))
    
    # Scatter plot of all random portfolios
    scatter = plt.scatter(portfolio_risks, portfolio_returns,
                          c=sharpe_ratios, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label='Sharpe Ratio')

    # Highlight the Maximum Sharpe Ratio Portfolio
    if max_sharpe_portfolio is not None:
        plt.scatter(max_sharpe_portfolio["Risk (Volatility)"],
                    max_sharpe_portfolio["Expected Return"],
                    color='red', marker='*', s=300,
                    label='Max Sharpe Ratio Portfolio')

    plt.title("Efficient Frontier & Random Portfolios")
    plt.xlabel("Risk (Volatility)")
    plt.ylabel("Expected Return")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_individual_asset_returns(returns):
    """
    Simple bar plot of individual asset average returns.
    Useful for comparison with optimized results.
    """
    mean_returns = returns.mean() * 252  # Annualized return (daily -> yearly)
    plt.figure(figsize=(8, 5))
    mean_returns.plot(kind='bar')
    plt.title("Annualized Returns of Individual Assets")
    plt.ylabel("Return")
    plt.grid(True, axis='y', linestyle='--', alpha=0.6)
    plt.show()
