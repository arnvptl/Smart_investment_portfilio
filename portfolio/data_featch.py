import yfinance as yf
from datetime import datetime,timedelta
import pandas as pd

def get_data(tickers,period_year):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=period_year*365)
    data = yf.download(tickers=tickers,start=start_date,end=end_date)['Close']
    data.dropna()
    return data
