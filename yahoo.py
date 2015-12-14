import pandas.io.data as web
import pandas as pd
import numpy as np
import datetime
from datetime import date
import psycopg2

host = 'localhost'
dbname = 'stocks'

username = 'postgres'
pw = 'postgres'
conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

print("Connected!\n")

start = datetime.datetime(2010,1,1)
today = datetime.datetime.today()
end = today


ticker = pd.read_csv('YahooStockTickerSymbols.csv', sep=';',encoding='utf8')
Exchange=pd.read_csv('YahooTickSymb.csv',sep=',',encoding='utf-8')
for i in range(len(Exchange)):
	command="""insert into exchange(exch,fjoldi,land,heimsalfa) values ('{}','{}','{}','{}')""".format(Exchange.iloc[i,0],Exchange.iloc[i,1],Exchange.iloc[i,2],Exchange.iloc[i,3])
	cursor.execute(command)
for i in range(len(ticker)):
	command="""insert into company(ticker,name,exchange,category) values ('{}','{}','{}','{}')""".format(ticker.iloc[i,0],ticker.iloc[i,1],ticker.iloc[i,2],ticker.iloc[i,3])
	print(command)
	cursor.execute(command)
	x = web.DataReader(ticker.iloc[i,0],'yahoo',start,end)
	for i in range(len(x)):
		command="""insert into data(ticker,date,open,high,low,close,volume,adjclose) values ('{}','{}','{}','{}','{}','{}','{}','{}')""".format(ticker,x.index[i],x.iloc[i,0],x.iloc[i,1],x.iloc[i,2],x.iloc[i,3],x.iloc[i,4],x.iloc[i,5])
		print(command)
		cursor.execute(command)

conn.commit()
cursor.close()
conn.close()