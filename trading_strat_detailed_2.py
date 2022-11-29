import numpy as np
import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
import yfinance as yf

pd.set_option('display.max_columns',10)

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
    daily_return_array = stock_df['daily_return'].to_numpy()
    for return_parameter in running_returns:
        running_returns_series = []
        for day in range(len(daily_return_array)):
            if day<return_parameter:
                running_returns_series.append(0)
            else:
                running_returns_series.append(np.mean(daily_return_array[(day-return_parameter):day]))
        stock_df[return_parameter] = running_returns_series
    return stock_df

def filter_stock_analysis(stock_df, start):
    stock_df = stock_df.drop(columns=['Open', 'High','Low','Close','Volume'])
    indexnum = stock_df.loc[stock_df['Date'] == start].index.values
    return stock_df.loc[int(indexnum):]

hist_data = stock_data_all(ticker, data_start, end)
hist_data_analysis = stock_data_analysis(hist_data, running_return_days)
data_analysis_filtered = filter_stock_analysis(hist_data_analysis, analysis_start)

print(data_analysis_filtered)


# stock_data = stock_data_in_range(hist_data, analysis_start)
# print(stock_data)