import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# create a data frame with daily returns (unadjusted) by stock ticker
def daily_returns(stocktickers, start_date, end_date):

    stock_dict = {}

    for stock in stocktickers:
        stock_df = pd.DataFrame(yf.download(stock, start_date, end_date))
        stock_df['daily_return'] = np.log(stock_df['Close'] / stock_df['Close'].shift(1))
        stock_dict[stock] = stock_df['daily_return']

    return pd.DataFrame(stock_dict)

def calc_portfolio_perfomance(stock_df, stocktickers, investment, investment_strat):

    stock_dict = {}
    for ticker in stocktickers:

        investment_series = [investment]
        running_investment = investment


    if investment_strat == "weekly_trend_follow":
        # if running seven days average is positive, invest. If not, hold.
        if stock_df[ticker][(days - 1)] > 0:
            running_investment = running_investment
        else:
            running_investment = running_investment * (1 + stock_df[ticker][days])
        investment_series.append(running_investment)


portfolio_stock_tickers = ['JNJ', 'LLY', 'PFE', 'ABBV', 'MRK']
start = '2010-01-01'
end = '2019-12-31'

print(daily_returns(portfolio_stock_tickers, start, end))
