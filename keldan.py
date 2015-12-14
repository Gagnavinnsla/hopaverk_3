from yahoo_finance import Share
import pandas as pd


ticker = pd.read_csv('YahooStockTickerSymbols.csv', sep=';',encoding='utf-8')

for i in ticker.iloc[0:16,0]:
print(i, Share(i).get_price())


#gætuð þurft að gera pip install yahoo_finance