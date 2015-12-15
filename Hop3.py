import pandas as pd 
import psycopg2
import getpass
import matplotlib.pyplot as plt
import numpy as np 
from numpy import matrix
from numpy import linalg
import pylab
from datetime import date
from datetime import timedelta
import RQ
from yahoo_finance import Share
from pandas_datareader import data as web


host = 'localhost'
dbname = 'stocks'

username = 'johanneshilmarsson'
pw = 'joijoi10'
conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()


#Valmynd
def printnames(Text) :
	Bool = False
	while Bool == False:
		cursor.execute(Text)
		F=cursor.fetchall()
		if F!=[]:
			Bool=True
		else:
			print('Nafnið er vitlaust eða gögn ekki til')
		for i in range(len(F)):
			print(i,F[i][0])
		Tmp=int(input())
		F=F[Tmp][0]
	return F
print("""Góðan daginn,
Velkominn í Ultra-Super-Mega-Giga-Undestructable-Uber-Portfolio Calculator
""")

Chosen=False
while Chosen==False:
	x=input("""Markaðurinn (Veldu: 1)\nFjárfestingarráðgjöf (Veldu 2)\nSpila Ping-Pong Veldu 3\n""")
	if x.isdigit():
		if int(x)==1:
			Chosen=True
		elif int(x)==2:
			Chosen=True
		elif int(x)==3:
			Chosen=True
		else:
			print('Veldu eitthvað af valmöguleikunum')
	else:
			print('Veldu eitthvað af valmöguleikunum')



x=int(x)
if x==2:
	
	Worked=False
	while Worked==False:
		try:
			Chosen=int(input("""Hversu langt tímabil viltu skoða:\nEitt ár(1) \nÞrjú ár(2) \nFimm ár (3) """))
			if Chosen==1:
				Timeformat=date.today()-timedelta(days=365)
				Worked=True
			elif Chosen==2:
				Timeformat=date.today()-timedelta(days=3*365)
				Worked=True
			elif Chosen==3:
				Worked=True
				Timeformat=date.today()-timedelta(days=5*365)
		except ValueError:
			continue

	Worked=False
	while Worked==False:
		try:
			Chosen=int(input("""Veldu stærð gagnagrunns fyrir portfolio:\nHeimsálfa (1) \nLand (2) \nMarkað (3) """))
			if Chosen==1:
				F=printnames('select DISTINCT e.heimsalfa from exchange e')
				Worked=True
				cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.heimsalfa like '{}' 
					and '{}' """.format(F,Timeformat))
				F=cursor.fetchall()
			elif Chosen==2:
				print("Veldu heimsálfu: ")
				F=printnames('select DISTINCT e.heimsalfa from exchange e')
				print("Veldu land: ")
				F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
				Worked=True
				cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.land like '{}' 
					and d.dags > '{}' """.format(F,Timeformat))			
				F=cursor.fetchall()			
			elif Chosen==3:
				print("Veldu heimsálfu: ")
				F=printnames('select DISTINCT e.heimsalfa from exchange e')
				print("Veldu land: ")
				F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
				print("Veldu markað: ")
				F=printnames("""select Distinct e.exch from exchange e where e.land like '%{}%'""".format(F))
				Worked=True
				cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker 
				where e.exch like '%{}%' and d.dags > '{}' """.format(F,Timeformat))			
				F=cursor.fetchall()
		except ValueError:
			continue
	#Bæta við áhættusækni??
print(F[-1][1])
if F[-1][1]=='HAGA.IC':
	print('Iceland!!')
	rf=0.065
else:
	rf=0.03

df = pd.DataFrame(F)
df = df.pivot(index=0,columns=1,values=2)
daily_retvec = (df - df.shift(1))/df
daily_expret = daily_retvec.mean()

yearly_expret = daily_expret*252
covmat = daily_retvec.cov()*252
yearly_vol = daily_retvec.std()*np.sqrt(252)
yearly_var = daily_retvec.var()*252


if x==1:
	Worked=False
	while Worked==False:
		try:
			x=int(input("""Veldu hvað þú vilt sjá:\n (1) Daginn í dag\n(2) Portfolio\n(3) Annað\n"""))
			if x==1:
				Worked=True
				start = date.today()-timedelta(days=7)
				end = date.today()
				innlestur = ['^GSPC', '^DJI', '^IXIC']
				dix={}
				for i in innlestur:
				    dix[i]=web.DataReader(i,'yahoo',start,end)
				df = pd.Panel(dix).minor_xs('Adj Close')
				dfx = pd.concat([df, df.pct_change()], axis=1).dropna()
				colms = [['S&P 500', 'Dow Jones Industrial','NASDAQ 100']['Adj Close', 'Daily Return']]
				multidx = pd.MultiIndex.from_product(colms)
				dfx.columns = multidx
				print('Helstu vísitölur: \n', dfx)
				#input heimsalfa -> land -> exchange -> ticker




				df = web.DataReader('AAPL','yahoo',start,end)
				dfb = web.DataReader('^GSPC','yahoo',start,end)
				df = pd.Panel(dix).minor_xs('Adj Close')
				dfb = pd.Panel(dix).minor_xs('Adj Close')
				dfret = df.pct_change()
				dfret = dfret.dropna()
				dfbret = dfb.pct_change()
				dfbret = dfbret.dropna()
				dfx=pd.concat([df,dfret,dfb,dfbret],axis=1)
				cols = [['Apple Inc','S&P 500'],['Adj Close', 'Daily Return']]
				multi_idx = pd.MultiIndex.from_product(cols)
				dfx.columns = cols
				dfx = dfx.dropna()
				covmat = pd.concat([dfret,dfbret],axis=0).cov()
				beta = covmat[0,1]/covmat[1,1]
				alpha = np.mean(dfret)-beta*np.mean(dfbret)
				volatility = np.sqrt(covmat[0,0])
				momentum = np.prod(1+dfret.tail(12).values)-1
				prd = 12
				alpha = alpha*prd
				volatility = volatility*np.sqrt(prd)
				plt.plot(dfret,dfbret)
				plt.ylabel('Price')
				plt.xlabel('Time')
				plt.show()
			elif x==2:
				Portfolio=pd.read_csv('Portfolio.csv',sep=';',encoding='utf8')
				Worked=True
				#Internet HAX
			elif x==3:
				Worked=True
				#Internet HaX
				print('Muahahahah')
		except ValueError:
			continue

covmat.fillna(0,inplace=True)
inv = matrix(covmat).I
#yearly_expret[yearly_expret>2.2 or yearly_expret<-1] = 0
for i in range(len(yearly_expret)):
	if yearly_expret[i]>1.5:
		yearly_expret[i]=0
	elif yearly_expret[i]<-1:
		yearly_expret[i]=0
a = (matrix(yearly_expret).T)

one = []
for i in range(len(a)):
	one.append(1)
one = matrix(one).T

A = matrix([[(a.T*inv*a).item(0), (a.T*inv*one).item(0)], [(a.T*inv*one).item(0), (one.T*inv*one).item(0)]])
AI = A.I

list1=np.arange(0,2,0.1)

std = []
for i in range(len(list1)):
	std.append(((matrix([[list1[i],1]])*AI*matrix([[list1[i],1]]).T).item(0))**0.5)

Aone = np.hstack([a, one])

w = []
for i in range(len(list1)):
	w.append(inv*Aone*AI*matrix([[list1[i],1]]).T)

MarketReturn=((a-rf).T*inv*(a-rf)).item(0)/(one.T*inv*(a-rf)).item(0)
VigtMarket=inv*Aone*AI*matrix([[MarketReturn,1]]).T
StdMarket=((matrix([[MarketReturn,1]])*AI*matrix([[MarketReturn,1]]).T).item(0))**0.5
wMarket=np.arange(0,1.5,0.1)
ReturnCML=[]
StdCML=[]
for i in range(len(wMarket)):
	ReturnCML.append(wMarket[i]*MarketReturn+(1-wMarket[i])*rf)
	StdCML.append(wMarket[i]*StdMarket)

Tickers=pd.DataFrame(yearly_expret.index.get_values())
def printweight(PortfolioSTD,VigtMarket,StdMarket,Tickers):
	Weight=PortfolioSTD/StdMarket
	VigtPortfolio=pd.DataFrame(Weight*VigtMarket)
	S=pd.DataFrame(columns=('Tickers','Weights'))
	S.loc[i]=['RiskFree',(1-Weight)]
	VigtPortfolio=pd.concat([Tickers,VigtPortfolio],axis=1)
	VigtPortfolio.columns=('Tickers','Weights')
	VigtPortfolio=VigtPortfolio.append(S)
	VigtPortfolio.to_csv('Portfolio.csv')
	print(VigtPortfolio)
	return PortfolioSTD,Weight

if input("""Ef þú ert vanur ýttu á 1, ef ekki ýttu á eitthvað annað"""))==isdigit(1)
	Bool=True
	while Bool:
		try:
			x=input("Hvort viltu ákvarða útfrá STD (1) eða E(r) (2)"))
			if x==1:
				E=int(input("Sláðu inn staðalfrávikið"))
				PortfolioSTD,Weight=printweight(E,VigtMarket,StdMarket,Tickers)
				Bool=False
			elif x==2:
				E=int(input("Sláðu inn vænta ávöxtun"))
				PortfolioSTD=((1-(E-rf))/(rf-MarketReturn))*StdMarket
				PortfolioSTD,Weight=printweight(PortfolioSTD,VigtMarket,StdMarket,Tickers)
				Bool=False
		except ValueError:
			continue
else:
	Bool=True
	while Bool==True:
		Risk=RQ.Quiz()
		if Risk=='A':
			PortfolioSTD,Weight=printweight(0.25,VigtMarket,StdMarket,Tickers)
			Bool=False
		elif Risk=='B':
			PortfolioSTD,Weight=printweight(0.16,VigtMarket,StdMarket,Tickers)
			Bool=False
		elif Risk=='C':
			PortfolioSTD,Weight=printweight(0.12,VigtMarket,StdMarket,Tickers)
			Bool=False
		elif Risk=='D':
			PortfolioSTD,Weight=printweight(0.05,VigtMarket,StdMarket,Tickers)
			Bool=False
		elif Risk=='E':
			PortfolioSTD,Weight=printweight(0,VigtMarket,StdMarket,Tickers)
			Bool=False
		else:
			print('Try again')
plt.plot(PortfolioSTD,(Weight*MarketReturn+(1-Weight)*rf),'o')		
plt.plot(StdCML,ReturnCML,'-')
plt.plot(std, list1, '-')
#plt.axis([0,0.25,0,1.25])
plt.ylabel('mean')
plt.xlabel('std')
print(yearly_expret)
pylab.show()
