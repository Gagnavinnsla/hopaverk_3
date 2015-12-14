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
		x=int(input("""Veldu stærð gagnagrunns fyrir portfolio:\n Heimsálfa(1)\nLand(2)\nMarkað(1)"""))
		if x==1:
			F=printnames('select DISTINCT e.heimsalfa from exchange e')
			Worked=True
		elif x==2:
			F=printnames('select Distinct e.land from exchange e')
			Worked=True
		elif x==3:
			F=printnames('select Distinc e.exch from exchange e')
			Worked=True