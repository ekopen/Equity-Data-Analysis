import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def stock_return_data(stocktickers, start_date, end_date):

    stock_dict = {}

    for stock in stocktickers:
        stock_df = pd.DataFrame(yf.download(stock, start_date, end_date))
        stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))
        stock_dict[stock] = stock_df['daily_return']
    return pd.DataFrame(stock_dict)

def long_strat(stock_long_df, stocktickers, investment):
#can probably get rid of the need to reimport tickers
    stock_dict = {}

    for ticker in stocktickers:

        investment_series = [investment]
        running_investment = investment

        for days in range(1,len(stock_long_df)):
            running_investment = running_investment * (1+stock_long_df[ticker][days])
            investment_series.append(running_investment)
        stock_long_df['portfolio value'] = investment_series
        stock_dict[ticker] = stock_long_df['portfolio value']

    return pd.DataFrame(stock_dict)

healthcare_stock_tickers = ['UNH', 'CI', 'ELV', 'CNC', 'HUM']
# healthcare_stock_names = ["United Health", "Cigna", "Elevance", "Centene", "Humana"]
start = '2019-01-01'
end = '2019-12-31'
starting_amount = 1000

#need to get the portfolio returns dataframe to stay static when running throuhg another function
portfolioreturns = stock_return_data(healthcare_stock_tickers, start, end)
longportfolio = long_strat(portfolioreturns, healthcare_stock_tickers, starting_amount)


# portfolio.plot()
# plt.show()
