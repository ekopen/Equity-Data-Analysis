import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

def stock_data(stocks, start_date, end_date, investment):
    stock_dict = {}
    for stock in stocks:

        stock_df = pd.DataFrame(yf.download(stock, start_date, end_date))
        stock_df['daily_return'] = np.log(stock_df['Adj Close'] / stock_df['Adj Close'].shift(1))

        investment_series = [investment]
        running_investment = investment

        for days in range(1,len(stock_df)):
            running_investment = running_investment * (1+stock_df['daily_return'][days])
            investment_series.append(running_investment)
        stock_df['portfolio value'] = investment_series
        stock_dict[stock] = stock_df['portfolio value']

    return pd.DataFrame(stock_dict)

healthcare_stocks = ['UNH', 'CI', 'ELV', 'CNC', 'HUM']
start = '2010-01-01'
end = '2019-12-31'
starting_amount = 1000

portfolio = stock_data(healthcare_stocks, start, end, starting_amount)
print(portfolio)
portfolio.plot()
plt.show()
