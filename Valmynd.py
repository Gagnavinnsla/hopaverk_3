import pandas as pd 
import psycopg2
import getpass
import matplotlib.pyplot as plt
import numpy as np 
from numpy import matrix
from scipy import linalg
import pylab


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
	x=input("""Skoða markaðinn (Veldu 1)\nBúa til portfolio (Veldu 2)\nSpila Ping-Pong Veldu (3)\n""")
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
		T=int(input("""Veldu stærð gagnagrunns fyrir portfolio:\n Heimsálfa(1)\nLand(2)\nMarkað(3)"""))
		if T==1:
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			Worked=True
			cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.heimsalfa like '{}' """.format(F))
			F=cursor.fetchall()
		elif T==2:
			print("Veldu Heimsálfu: ")
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			print("Veldu land: ")
			F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
			Worked=True
			cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.land like '{}' """.format(F))			
			F=cursor.fetchall()			
		elif T==3:
			print("Veldu Heimsálfu: ")
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			print("Veldu land: ")
			F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
			print("Veldu Markað: ")
			F=printnames("""select Distinct e.exch from exchange e where e.land like '%{}%'""".format(F))
			Worked=True
			cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.exch like '{}' """.format(F))			
			F=cursor.fetchall()
	#Bæta við áhættusækni??

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
inv = linalg.inv(covmat)
print(inv)
yearly_expret[np.isneginf(yearly_expret)] = 0
a = (matrix(yearly_expret).T)

one = []
for i in range(len(a)):
	one.append(1)
one = matrix(one).T

A = matrix([[(a.T*inv*a).item(0), (a.T*inv*one).item(0)], [(a.T*inv*one).item(0), (one.T*inv*one).item(0)]])
AI = A.I

list1=[]
list1.append(0)
for i in range(1,50):
	list1.append(list1[i-1]+0.01)

std = []
for i in range(len(list1)):
	std.append(((matrix([[list1[i],1]])*AI*matrix([[list1[i],1]]).T).item(0))**0.5)

Aone = np.hstack([a, one])

print(Aone)

w = []
for i in range(len(list1)):
	w.append(inv*Aone*AI*matrix([[list1[i],1]]).T)

print(std)
plt.plot(std, list1, 'o')
plt.ylabel('mean')
plt.xlabel('std')
pylab.show()
