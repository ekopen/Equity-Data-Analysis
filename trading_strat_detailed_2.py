import numpy as np
import pandas as pd
from numpy import mean
import matplotlib.pyplot as plt
import yfinance as yf

pd.set_option('display.max_columns',10)

ticker = 'SPY'
data_start = '2000-01-03'
#start date for pulling all stock data
analysis_start = '2010-01-04'
#start date for the date subset for analysis
end = '2015-12-31'
running_return_spans = [2,5,10,20]
#day spans of average returns in the analysis function
portfolio_amt = 1000
strategies = ['Long', 'Trend_Follow', 'Trend_Reverse']


def stock_data_all(stockticker, start_date, end_date):
    #initialize the stock data from Yahoo Finance
    stock_df = pd.DataFrame(yf.download(stockticker, start_date, end_date))
    return stock_df.reset_index()

def stock_analysis(stock_df, running_return_spans):
    #append columns that contain different data useful for analysis
    stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))
    daily_return_array = stock_df['daily_return'].to_numpy()
    for return_span in running_return_spans:
        running_returns_series = []
        for day in range(len(daily_return_array)):
            if day<return_span:
                running_returns_series.append(0)
            else:
                running_returns_series.append(np.mean(daily_return_array[(day-return_span):day]))
        stock_df[return_span] = running_returns_series
    return stock_df

def stock_analysis_filtered(stock_df, start):
    stock_df = stock_df.drop(columns=['Open', 'High','Low','Close','Volume'])
    indexnum = stock_df.loc[stock_df['Date'] == start].index.values
    return stock_df.loc[int(indexnum):].reset_index()

def calc_pf_performance(stock_df, portfolio_amt, running_return_spans, strategies):

    for strat in strategies:

        if strat == 'Long':
            portfolio_series = []
            running_portfolio_amt = portfolio_amt
            for day in range(len(stock_df['daily_return'])):
                running_portfolio_amt = running_portfolio_amt * (1 + stock_df['daily_return'][day])
                portfolio_series.append(running_portfolio_amt)
            stock_df[strat] = portfolio_series

        if strat == 'Trend_Follow':
            for return_span in running_return_spans:
                portfolio_series = []
                running_portfolio_amt = portfolio_amt
                for day in range(len(stock_df[return_span])):
                    if stock_df[return_span][day]>0:
                        running_portfolio_amt = running_portfolio_amt * (1+stock_df['daily_return'][day])
                    else:
                        running_portfolio_amt = running_portfolio_amt
                    portfolio_series.append(running_portfolio_amt)
                stock_df[str(return_span) + ' ' + strat] = portfolio_series

        if strat == 'Trend_Reverse':
            for return_span in running_return_spans:
                portfolio_series = []
                running_portfolio_amt = portfolio_amt
                for day in range(len(stock_df[return_span])):
                    if stock_df[return_span][day]<0:
                        running_portfolio_amt = running_portfolio_amt * (1+stock_df['daily_return'][day])
                    else:
                        running_portfolio_amt = running_portfolio_amt
                    portfolio_series.append(running_portfolio_amt)
                stock_df[str(return_span) + ' ' + strat] = portfolio_series

    return stock_df




hist_data = stock_data_all(ticker, data_start, end)
hist_data_analysis = stock_analysis(hist_data, running_return_spans)
data_analysis_filtered = stock_analysis_filtered(hist_data_analysis, analysis_start)
data_analysis_filtered.to_pickle("./stock_data.pkl")

portfolio_data = calc_pf_performance(pd.read_pickle("./stock_data.pkl"),portfolio_amt,running_return_spans,strategies)
portfolio_data_filtered = portfolio_data.drop(columns=['Date', 'Adj Close','daily_return',2,5,10,20])
print(portfolio_data_filtered)

