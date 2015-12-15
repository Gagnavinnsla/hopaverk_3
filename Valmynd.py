import pandas as pd 
import psycopg2
import getpass
import matplotlib.pyplot as plt
import numpy as np 
from numpy import matrix
from scipy import linalg
import pylab
from datetime import date
from datetime import timedelta


host = 'localhost'
dbname = 'stocks'

username = 'johanneshilmarsson'
pw = 'joijoi10'
conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, pw)

print("Connecting to database {}.{} as {}".format(host, dbname, username))

conn = psycopg2.connect(conn_string)

cursor = conn.cursor()

\
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
			Chosen=int(input("""Hversu langt tímabil viltu skoða:\nEitt ár(1) \nTvö ár(2) \nÞrjú ár (3) """))
			if Chosen==1:
				Timeformat=date.today()-timedelta(days=365)
				Worked=True
			elif Chosen==2
				Timeformat=date.today()-timedelta(days=3*365)
				Worked=True
			elif Chosen==3
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
if F[-1][1]==ICEX:
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
				innlestur = ['^GSPC', '^DJI', '^IXIC']
				yah = web.DataReader(innlestur,'yahoo',date.today(),date.today())
				print(yah)
				#INTERNET HAX
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
print(inv)
yearly_expret[np.isneginf(yearly_expret)] = 0
a = (matrix(yearly_expret).T)

one = []
for i in range(len(a)):
	one.append(1)
one = matrix(one).T

A = matrix([[(a.T*inv*a).item(0), (a.T*inv*one).item(0)], [(a.T*inv*one).item(0), (one.T*inv*one).item(0)]])
AI = A.I

list1=np.arange(0,0.5,0.01)

std = []
for i in range(len(list1)):
	std.append(((matrix([[list1[i],1]])*AI*matrix([[list1[i],1]]).T).item(0))**0.5)

Aone = np.hstack([a, one])

print(Aone)

w = []
for i in range(len(list1)):
	w.append(inv*Aone*AI*matrix([[list1[i],1]]).T)

MarketReturn=((a-rf).T*inv*(a-rf)).item(0)/(one*inv*(a-e)).item(0)
VigtMarket=inv*Aone*AI*matrix([[MarketReturn,1]]).T
StdMarket=((matrix([[MarketReturn,1]])*AI*matrix([[MarketReturn,1]]).T).item(0))**0.5
wMarket=np.arrange(0,2,0.1)
ReturnCML=[]
StdCML=[]
for i in range(len(wMarket)):
	ReturnCML.append(w*Marketreturn+(1-w)*rf)
	StdCML.append=(w*StdMarket)


plt.plot(std, list1, '-o')
plt.axis([0,0.5,0,1])
plt.ylabel('mean')
plt.xlabel('std')
plt.plot(StdCML,ReturnCML,'-y')
pylab.show()
