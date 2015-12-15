import pandas as pd 
import psycopg2
import getpass

host = 'localhost'
dbname = 'stocks'

username = 'postgres'
pw = 'postgres'
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
		x=int(input("""Veldu stærð gagnagrunns fyrir portfolio:\n Heimsálfa(1)\nLand(2)\nMarkað(3)"""))
		if x==1:
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			Worked=True
			cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.heimsalfa like '{}' """.format(F))
			F=cursor.fetchall()
		elif x==2:
			print("Veldu Heimsálfu: ")
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			print("Veldu land: ")
			F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
			Worked=True
			cursor.execute("""select d.dags, d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.land like '{}' """.format(F))			
			F=cursor.fetchall()			
		elif x==3:
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
daily_ret = df.pct_change()
daily_expret = daily_ret.mean()
yearly_expret = daily_ret.mean()*sqrt(252)



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
