import pandas as pd

df = pd.read_csv(r'C:\Users\erict\PycharmProjects\stock_trading_simulator\symbols_valid_meta.csv')
df = df.iloc[:,1:3].to_pickle("./ticker_name_key.pkl")

print(df)