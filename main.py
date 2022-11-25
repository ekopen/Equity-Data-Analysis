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

# run the daily returns data frame through different simple investment strategies
def calc_portfolio_perfomance(stock_df, stocktickers, investment, investment_strat):

    stock_dict = {}
    for ticker in stocktickers:

        investment_series = [investment]
        running_investment = investment

        for days in range(1,len(stock_df)):
            if investment_strat == "long_strat":
                # buy and hold
                running_investment = running_investment * (1+stock_df[ticker][days])
                investment_series.append(running_investment)
            if investment_strat == "positive_trend_strat":
                # if stock goes down the previous day, take out investment. If not, reinvest.
                if stock_df[ticker][(days - 1)] < 0:
                    running_investment = running_investment
                else:
                    running_investment = running_investment * (1 + stock_df[ticker][days])
                investment_series.append(running_investment)
            if investment_strat == "anti_trend_strat":
                # if stock goes up the previous day, take out investment. If not, reinvest.
                if stock_df[ticker][(days - 1)] > 0:
                    running_investment = running_investment
                else:
                    running_investment = running_investment * (1 + stock_df[ticker][days])
                investment_series.append(running_investment)
        stock_df['portfolio value'] = investment_series
        stock_dict[ticker] = stock_df['portfolio value']

    return pd.DataFrame(stock_dict)

# initialize the portfolio
portfolio_stock_tickers = ['JNJ', 'LLY', 'PFE', 'ABBV', 'MRK']
start = '2010-01-01'
end = '2019-12-31'
# maybe clarify this is per stock, create ways to weigh it
starting_amount = 1000

# get the returns data frame and serialize it before passing through future functions
portfolio_returns = daily_returns(portfolio_stock_tickers, start, end)
portfolio_returns.to_pickle("./daily_returns.pkl")
print(portfolio_returns)

# create data frames for the different strategies and return a sum column
trading_strats = ["long_strat", "positive_trend_strat", "anti_trend_strat"]
portfolios = []
for strat in trading_strats:
    portfolios.append(calc_portfolio_perfomance(pd.read_pickle("./daily_returns.pkl"), portfolio_stock_tickers,
                                                 starting_amount, strat).sum(axis=1))

# combine into a single data frame and plot it
portfolio_combos = pd.concat(portfolios, keys=["Long Only", "Trend Follow", "Trend Reverse"], axis = 1, join="inner")
print(portfolio_combos)
portfolio_combos.plot()
plt.show()

# work on further interpreting this part
#test


