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
			cursor.execute("""select d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.heimsalfa like '{}' """.format(F))
			F=cursor.fetchall()
		elif x==2:
			print("Veldu Heimsálfu: ")
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			print("Veldu land: ")
			F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
			Worked=True
			cursor.execute("""select d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.land like '{}' """.format(F))			
			F=cursor.fetchall()			
		elif x==3:
			print("Veldu Heimsálfu: ")
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			print("Veldu land: ")
			F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
			print("Veldu Markað: ")
			F=printnames("""select Distinct e.exch from exchange e where e.land like '%{}%'""".format(F))
			Worked=True
			cursor.execute("""select d.ticker,d.adjclose from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.exch like '{}' """.format(F))			
			F=cursor.fetchall()

x = int(x)
if x == 3:
	Worked = False
	while Worked==False:
		x = int(input("""Veldu hvað þú vilt gera:\n (1) Skoða ákveðin markað\n (2) Fjöldi markaða frá hverju landi\n (3) Fjöldi markaða frá hverri Heimsálfu  \n (4) Fjöldi fyrirtækja í landi\n (5) Fjöldi fyrirtæka í heimsálfu"""))
		if x == 1:
			F = printnames('select DISTINCT e.exch, e.land FROM  exchange e')
			Worked = True
			cursor.execute("""select c.exchange, c.ticker,c.name,c.category,e.heimsalfa,e.land from company c JOIN exchange e ON c.exchange = e.exch JOIN data d ON c.ticker = d.ticker where e.exch like '%{}%' """.format(F))
			F=cursor.fetchall()
			F = pd.DataFrame(F)
			F.columns=['Markaður','Ticker','Nafn','Atvinnugrein','Heimálfa','Land']
			print(F)
		if x == 2:
			Worked = True
			cursor.execute("""select e.land, count(e.exch) from exchange e GROUP BY e.land ORDER BY count(e.exch) DESC""")
			F=cursor.fetchall()
			df = pd.DataFrame(F, columns=['Lönd','Fjöldi markaða'])
			print (df)
		if x == 3:
			Worked = True
			cursor.execute("""select e.heimsalfa, count(e.exch) from exchange e GROUP BY e.heimsalfa ORDER BY count(e.exch) DESC""")
			F=cursor.fetchall()
			df = pd.DataFrame(F,columns=['Heimsálfur','Fjöldi markaða'])
			print (df)
		if x == 4:
			print('\n Veldu Heimsálfu: \n')
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			Worked = True
			print('\n Veldu land: \n')

			F=printnames("""select Distinct e.land from exchange e where e.heimsalfa like '%{}%'""".format(F))
			cursor.execute("""select e.land,e.exch,count(c.name) from company c join exchange e ON c.exchange = e.exch where e.land like '%{}%' GROUP BY e.exch,e.land ORDER BY count(c.name) DESC""".format(F))
			F=cursor.fetchall()
			df = pd.DataFrame(F,columns=['Lönd','Markaðir','Fjöldi Fyrirtæki'])
			print (df)
		if x == 5:
			print('\n Veldu Heimsálfu: \n')
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			Worked = True
			cursor.execute("""select e.heimsalfa, e.land,e.exch,count(c.name) from company c join exchange e ON c.exchange = e.exch where e.heimsalfa like '%{}%' GROUP BY e.exch,e.land ORDER BY count(c.name) DESC""".format(F))
			F=cursor.fetchall()
			df = pd.DataFrame(F,columns=['Heimsálfa','Lönd','Markaðir','Fjöldi Fyrirtæki'])
			print (df)