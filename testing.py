import numpy as np
import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
import yfinance as yf

stockticker = 'WMT'
historic_start = '2000-01-01'
start = '2015-01-02'
end = '2019-12-31'

def stock_historical_data(stockticker, start_date, end_date):
    #initialize the stock data from Yahoo Finance

    stock_dict = {}
    stock_df = pd.DataFrame(yf.download(stockticker, start_date, end_date))
    stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))
    return stock_df.reset_index()

def stock_data_in_range(stock_df, start):
    #these locs are unneeded. not sure why.
    indexnum = stock_df.loc[stock_df['Date'] == start].index.values
    return stock_df.loc[int(indexnum):]

#create rolling returns columns


hist_data = stock_historical_data('SPY', historic_start, end)
# this loc is unneeded. not sure why.
print(hist_data.loc[hist_data['Date'] == '2015-01-02'])

stock_data = stock_data_in_range(hist_data, start)
print(stock_data)