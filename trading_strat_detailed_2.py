import numpy as np
import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
import yfinance as yf

ticker = 'SPY'
data_start = '2000-01-01'
#start date for pulling all stock data
analysis_start = '2015-01-02'
#start date for the date subset for analysis
end = '2019-12-31'
running_return_days = [2,5,10,20]
#day spans of average returns in the analysis function

def stock_data_all(stockticker, start_date, end_date):
    #initialize the stock data from Yahoo Finance
    stock_df = pd.DataFrame(yf.download(stockticker, start_date, end_date))
    return stock_df.reset_index()

def stock_data_analysis(stock_df, running_returns):
    #append columns that contain different data useful for analysis
    stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))
    for x in running_returns:
        running_returns_series = []
        for days in stock_df['daily_return']:
            #work on getting this to return a series with running average returns
            print(1)
    return stock_df

def stock_data_in_range(stock_df, start):
    #append the dataframe to only include relevant dates for analysis
    #these locs are unneeded. not sure why
    indexnum = stock_df.loc[stock_df['Date'] == start].index.values
    return stock_df.loc[int(indexnum):]




hist_data = stock_data_all(ticker, data_start, end)
hist_data_analysis = stock_data_analysis(hist_data, running_return_days)
print(hist_data_analysis)


# stock_data = stock_data_in_range(hist_data, analysis_start)
# print(stock_data)