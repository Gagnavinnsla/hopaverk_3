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
#That's Right

host = 'localhost'
dbname = 'stocks'

username = 'postgres'
pw = 'postgres'
conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()
#Classic connect

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
	x=input("""Markaðurinn (Veldu: 1)\nFjárfestingarráðgjöf (Veldu 2)\nÝmsar skipanir 3\n""")
	if x.isdigit():
		if int(x)==1:
			Chosen=True
		elif int(x)==2:
			Chosen=True
		elif int(x)==3:
			Chosen=True
		else:
			print('Veldu einhvern af valmöguleikunum')



x=int(x)
if x==1:
	Worked=False
	while Worked==False:
		try:
			Chosen=int(input("""Veldu hvað þú vilt sjá:\n (1) Daginn í dag\n(2) Portfolio\n(3) Annað\n"""))
			if Chosen==1:
				Worked=True
				start = date.today()-timedelta(days=7)
				end = date.today()
				innlestur = ['^GSPC', '^DJI', '^IXIC']
				dix={}
				for i in innlestur:
				    dix[i]=web.DataReader(i,'yahoo',start,end)
				df = pd.Panel(dix).minor_xs('Adj Close')
				dfx = pd.concat([df, df.pct_change()], axis=1).dropna()
				colms = ['S&P 500', 'Dow Jones Industrial','NASDAQ 100','S&P500 - Daily %', 'DJI - Daily %','NASDAQ100 - Daily %']
				print('Helstu vísitölur: \n', dfx)
				#input heimsalfa -> land -> exchange -> ticker
				print("Veldu heimsálfu: ")
				F=printnames('select DISTINCT e.heimsalfa from exchange e')
				print("Veldu land: ")
				F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
				print("Veldu markað: ")
				F=printnames("""select Distinct e.exch from exchange e where e.land like '%{}%'""".format(F))
				print("Veldu Ticker: ")
				F=printnames("""select DISTINCT d.ticker from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker 
				where e.exch like '%{}%' """.format(F))

				df = web.DataReader(F,'yahoo',start,end)
				dfb = web.DataReader('^GSPC','yahoo',start,end)
				df = df.ix[0:,5:6]
				dfb = dfb.ix[0:,5:6]
				dfret = df.pct_change().dropna()
				dfbret = dfb.pct_change().dropna()
				matret = pd.concat([dfret,dfbret],axis=1)
				matret.columns = [F,' - Daily Return', 'S&P 500 - Daily Return']
				dfx=pd.concat([df,dfret,dfb,dfbret],axis=1)
				cols = ['Apple Inc - Adj Close','S&P 500 - Adj Close','Apple Inc - Daily Return', 'S&P 500 - Daily Return']
				dfx.columns = cols
				dfx = dfx.dropna()
				covmat = np.cov(matret)
				beta = covmat[0,1]/covmat[1,1]
				alpha = np.mean(dfret)-beta*np.mean(dfbret)
				volatility = np.sqrt(covmat[0,0])
				m200avg = np.mean(dfret.tail(200))
				m50avg = np.mean(dfret.tail(50))
				m25avg = np.mean(dfret.tail(25))
				week52high = max(dfret)
				week52low =min(dfret)
				timabil = 12
				ltm = (df.tail(1)-df.iloc[0,0])/df.iloc[0,0]
				alpha = alpha*timabil
				volatility = volatility*np.sqrt(timabil)
				sharpe = (np.mean(dfret)-0.02)/volatility
				treynor = (np.mean(dfret)-0.02)/beta
				plt.plot(dfret,dfbret)
				plt.ylabel('Price')
				plt.xlabel('Time')
				plt.show()
				print('\nÁvöxtun síðustu 12 mánaða: ',ltm, "\nStaðalfrávik: ", volatility,'\nBeta: ', beta,'\nAlpha-gildi: ',alpha,'\nHámarksverð síðustu 12 mánaða: ',week52high)
				print('\nLágmark síðustu 12 mánaða: ',week52low, '\n200 daga hlaupandi staðalfrávik: ', m200avg,'\n50 daga hlaupandi staðalfrávik: ',m50avg)
				print('\n25 daga hlaupandi staðalfrávik: ',m25avg,'\nSharpe-hlutfall: ',sharpe,'\nTreynor-hlutfall: ',treynor,'\nSamdreifnifylki: ', covmat)


			elif Chosen==2:
				Portfolio=pd.read_csv('Portfolio.csv',sep=',',encoding='utf8')
				Worked=True
				start = date(2015,12,12)
				end = date.today()
				dix = {}
				for i in Portfolio['Tickers'][:-1]:
					dix[i] = web.DataReader(i,'yahoo',start,end)
					print(i,Share(i).get_price(), Share(i).get_eps())

			elif Chosen == 3:
				Worked = False
				while Worked==False:
					Chosen = int(input("""Veldu hvað þú vilt gera:\n (1) Skoða ákveðin markað\n (2) Fjöldi markaða frá hverju landi\n (3) Fjöldi markaða frá hverri Heimsálfu  \n (4) Fjöldi fyrirtækja í landi\n (5) Fjöldi fyrirtæka í heimsálfu"""))
					if Chosen == 1:
						F = printnames('select DISTINCT e.exch, e.land FROM  exchange e')
						Worked = True
						cursor.execute("""select c.exchange, c.ticker,c.name,c.category,e.heimsalfa,e.land from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.exch like '%{}%' """.format(F))
						F=cursor.fetchall()
						F = pd.DataFrame(F)
						F.columns=['Markaður','Ticker','Nafn','Atvinnugrein','Heimálfa','Land']
						print(F)
					elif Chosen == 2:
						Worked = True
						cursor.execute("""select e.land, count(e.exch) from exchange e GROUP BY e.land ORDER BY count(e.exch) DESC""")
						F=cursor.fetchall()
						df = pd.DataFrame(F, columns=['Lönd','Fjöldi markaða'])
						print (df)
					elif Chosen == 3:
						Worked = True
						cursor.execute("""select e.heimsalfa, count(e.exch) from exchange e GROUP BY e.heimsalfa ORDER BY count(e.exch) DESC""")
						F=cursor.fetchall()
						df = pd.DataFrame(F,columns=['Heimsálfur','Fjöldi markaða'])
						print (df)
					elif Chosen == 4:
						print('\n Veldu Heimsálfu: \n')
						F=printnames('select DISTINCT e.heimsalfa from exchange e')
						Worked = True
						print('\n Veldu land: \n')

						F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
						cursor.execute("""select e.land,e.exch,count(c.name) from company c join exchange e ON c.exchange = e.exch where e.land like '%{}%' GROUP BY e.exch,e.land ORDER BY count(c.name) DESC""".format(F))
						F=cursor.fetchall()
						df = pd.DataFrame(F,columns=['Lönd','Markaðir','Fjöldi Fyrirtækja'])
						print (df)
					elif Chosen == 5:
						print('\n Veldu Heimsálfu: \n')
						F=printnames('select DISTINCT e.heimsalfa from exchange e')
						Worked = True
						cursor.execute("""select e.heimsalfa, e.land,e.exch,count(c.name) from company c join exchange e ON c.exchange = e.exch where e.heimsalfa like '%{}%' GROUP BY e.exch,e.land ORDER BY count(c.name) DESC""".format(F))
						F=cursor.fetchall()
						df = pd.DataFrame(F,columns=['Heimsálfa','Lönd','Markaðir','Fjöldi Fyrirtækja'])
						print (df)


elif x == 2:
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
				name=F
				cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.heimsalfa like '{}' 
					and '{}' """.format(F,Timeformat))
				F=cursor.fetchall()
			elif Chosen==2:
				print("Veldu heimsálfu: ")
				F=printnames('select DISTINCT e.heimsalfa from exchange e')
				print("Veldu land: ")
				F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
				Worked=True
				name=F
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
				name=F
				cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker 
				where e.exch like '%{}%' and d.dags > '{}' """.format(F,Timeformat))			
				F=cursor.fetchall()
		except ValueError:
				continue

	if F[-1][1]=='HAGA.IC':
		rf=0.065
	else:
		rf=0.02

	df = pd.DataFrame(F)
	df = df.pivot(index=0,columns=1,values=2)
	daily_retvec = (df - df.shift(1))/df
	daily_expret = daily_retvec.mean()

	yearly_expret = daily_expret*252
	covmat = daily_retvec.cov()*252
	yearly_vol = daily_retvec.std()*np.sqrt(252)
	yearly_var = daily_retvec.var()*252

	covmat.fillna(0,inplace=True)
	inv = matrix(covmat).I
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

	Returns=np.arange(0,2,0.1)

	std = []
	for i in range(len(Returns)):
		std.append(((matrix([[Returns[i],1]])*AI*matrix([[Returns[i],1]]).T).item(0))**0.5)

	Aone = np.hstack([a, one])

	w = []
	for i in range(len(Returns)):
		w.append(inv*Aone*AI*matrix([[Returns[i],1]]).T)

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

	if input("""Ef þú ert vanur ýttu á 1, ef ekki ýttu á eitthvað annað""")=='1':
		Bool=True
		while Bool:
			try:
				x=input("Hvort viltu ákvarða útfrá STD (1) eða E(r) (2)")
				if x=='1':
					E=float(input("Sláðu inn staðalfrávikið"))
					PortfolioSTD,Weight=printweight(E,VigtMarket,StdMarket,Tickers)
					Bool=False
				elif x=='2':
					E=float(input("Sláðu inn vænta ávöxtun"))
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
	for i in range(len(yearly_vol)):
		if yearly_vol[i]>0.6:
			yearly_vol[i]=0
			yearly_expret[i]=0
	plt.figure(num=None, figsize=(10, 10), dpi=80, facecolor='w', edgecolor='y')
	plt.plot(PortfolioSTD,(Weight*MarketReturn+(1-Weight)*rf),'o',linewidth = 6.0,label = 'Rálagt eignarsafn')		
	plt.plot(StdCML,ReturnCML,'-', label = 'Markaðslína')
	plt.plot(std, Returns, '-',label = 'Framfall')
	plt.plot(yearly_vol,yearly_expret, 'o',label = 'Fyrirtækin')
	plt.legend(loc = 'upper center',shadow = True)
	plt.title(name)s
	plt.axis([0,np.max(std),-0.3,np.max(Returns)])
	plt.ylabel('mean')
	plt.xlabel('std')

	pylab.show()


