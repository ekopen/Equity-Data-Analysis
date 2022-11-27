"""just a file to test random shtuff
    """

import numpy as np
import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
import yfinance as yf

def stock_data(stockticker, start_date, end_date):

    stock_dict = {}
    stock_df = pd.DataFrame(yf.download(stockticker, start_date, end_date))
    stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))
    stock_dict[stockticker] = stock_df[['Open', 'Adj Close', 'daily_return']].iloc[252:]
    return (stock_dict)

print

ticker = 'IBM'
start = '2009-01-01'
end = '2019-12-31'
investment = 1000

print(stock_data(ticker, start,end)['IBM']['daily_return'])