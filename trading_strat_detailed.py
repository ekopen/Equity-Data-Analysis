import numpy as np
import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
import yfinance as yf

def stock_data(stockticker, start_date, end_date):
    #initialize the stock data from Yahoo Finance

    stock_dict = {}
    stock_df = pd.DataFrame(yf.download(stockticker, start_date, end_date))
    stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))
    stock_dict[stockticker] = stock_df[['Open', 'Adj Close', 'daily_return']].iloc[252:]
    return (stock_dict)

def trend_following_strats(stock_dict, ticker, pf_value):
    """day to day strategy where we hold, buy, or sell at the adjusted close price
    daily decision is based on prevailing trend for an amount of preceding days
    for example, daily positive trend for the last three adjusted closes means you hold/buy until the trend is broken
    """

    pf_dict = {'returns':stock_dict[ticker]['daily_return'],'rolling_average':[], 'pf_value':[], 'action':[]}

    series_adjustment = 252
    # add this to get rid of stock data that only contributes to rolling averages
    trend_duration = 2
    #rolling average return time frame

    for days in range(0, len(stock_dict[ticker]['daily_return'])):
        if days < trend_duration:
            pf_dict['rolling_average'].append(0)
            pf_dict['action'].append(0)
            pf_dict['pf_value'].append(pf_value)
            #append 0s before we have enough historical data to begin
        else:
            pf_dict['rolling_average'].append(mean(stock_dict[ticker]['daily_return'][(days - trend_duration):days]))
            if pf_dict['rolling_average'][days] > 0:
                pf_dict['action'].append(1)
                pf_dict['pf_value'].append(pf_value * (1 + pf_dict['returns'][days]))
                pf_value = pf_dict['pf_value'][days]
                # if rolling average is positive, buy/hold
            else:
                pf_dict['action'].append(0)
                pf_dict['pf_value'].append(pf_value)
                # if rolling average is negative, sell

    return (pf_dict)

ticker = 'UNH'
start = '2009-01-01'
end = '2019-12-31'
investment = 1000

stock_dict = stock_data(ticker, start, end)
pf_dict = trend_following_strats(stock_dict, ticker, investment)
pf_return_df = pd.DataFrame(pf_dict['pf_value'])

print(pf_return_df)
pf_return_df.plot()
plt.show()