import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def daily_returns(stocktickers, start_date, end_date):

    stock_dict = {}

    for stock in stocktickers:
        stock_df = pd.DataFrame(yf.download(stock, start_date, end_date))
        stock_df['daily_return'] = np.log(stock_df['Close'] / stock_df['Close'].shift(1))
        stock_dict[stock] = stock_df['daily_return']

    return pd.DataFrame(stock_dict)

def long_strat(stock_df, stocktickers, investment):
#can probably get rid of the need to reimport tickers

    stock_dict = {}
    for ticker in stocktickers:

        investment_series = [investment]
        running_investment = investment

        for days in range(1,len(stock_df)):
            running_investment = running_investment * (1+stock_df[ticker][days])
            investment_series.append(running_investment)
        stock_df['portfolio value'] = investment_series
        stock_dict[ticker] = stock_df['portfolio value']

    return pd.DataFrame(stock_dict)

def positive_trend_strat(stock_df, stocktickers, investment):

    stock_dict = {}
    for ticker in stocktickers:

        investment_series = [investment]
        running_investment = investment

        for days in range(1, len(stock_df)):
            # #if stock goes down the previous day, take out investment. If not, reinvest.
            if stock_df[ticker][(days-1)] < 0:
                running_investment = running_investment
            else:
                running_investment = running_investment * (1 + stock_df[ticker][days])
            investment_series.append(running_investment)
        stock_df['portfolio value'] = investment_series
        stock_dict[ticker] = stock_df['portfolio value']

    return pd.DataFrame(stock_dict)

def anti_trend_strat(stock_df, stocktickers, investment):

    stock_dict = {}
    for ticker in stocktickers:

        investment_series = [investment]
        running_investment = investment

        for days in range(1, len(stock_df)):
            #if stock goes up the previous day, take out investment. If not, reinvest.
            if stock_df[ticker][(days-1)] > 0:
                running_investment = running_investment
            else:
                running_investment = running_investment * (1 + stock_df[ticker][days])
            investment_series.append(running_investment)
        stock_df['portfolio value'] = investment_series
        stock_dict[ticker] = stock_df['portfolio value']

    return pd.DataFrame(stock_dict)




portfolio_stock_tickers = ['JNJ', 'LLY', 'PFE', 'ABBV', 'MRK']
# healthcare_stock_names = ["United Health", "Cigna", "Elevance", "Centene", "Humana"]
start = '2015-01-01'
end = '2019-12-31'
starting_amount = 1000


portfolio_returns = daily_returns(portfolio_stock_tickers, start, end)
portfolio_returns.to_pickle("./daily_returns.pkl")
print(portfolio_returns)

long_portfolio = long_strat(pd.read_pickle("./daily_returns.pkl"), portfolio_stock_tickers, starting_amount).sum(axis=1)
positive_trend_portfolio = positive_trend_strat(pd.read_pickle("./daily_returns.pkl"), portfolio_stock_tickers, starting_amount).sum(axis=1)
anti_trend_portfolio = anti_trend_strat(pd.read_pickle("./daily_returns.pkl"), portfolio_stock_tickers, starting_amount).sum(axis=1)

portfolios = [long_portfolio, positive_trend_portfolio, anti_trend_portfolio]
portfolio_combos = pd.concat(portfolios, keys=["Long Only", "Trend Follow", "Trend Reverse"], axis = 1, join="inner")
print(portfolio_combos)

portfolio_combos.plot()
plt.show()


