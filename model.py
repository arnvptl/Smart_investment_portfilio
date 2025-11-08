import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import yfinance as yf
import seaborn as sns

tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
benchmark = "^GSPC"  # S&P 500 for beta calculation

data = yf.download(tickers,start="2024-01-01",end="2024-12-31")