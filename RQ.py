def Quiz():
	def getAnswer (answer, counter):
		if len(answer)!=1:
			return counter,True
		elif answer == 'a':
			counter += 1
			return counter,False
		elif answer == 'b':
			counter += 2
			return counter,False
		elif answer == 'c':
			counter += 3
			return counter,False
		elif answer == 'd':
			counter += 4
			return counter,False
		elif answer == 'e':
			counter += 5
			print('Enter')
			return counter,False
		else:
			return counter,True

	def nidurstada (counter):
		if counter >= 46:
			Notandi = 'A'
			print('Þú ert mjög áhættusækinn og því mælum við með:')
		elif counter > 40 and counter < 46:
			Notandi = 'B'
			print('Þú ert áhættusækinn og því mælum við með:')
		elif counter >= 36 and counter < 41:
			Notandi = 'C'
			print('Þú ert hlutlaus gagnvart áhættu og því mælum við með:')
		elif counter >= 31 and counter < 36:
			Notandi = 'D'
			print('Þú ert áhættufælinn eða ekki í aðstöðu til að taka áhættu og því mælum við með:')
		elif counter < 31:
			Notandi = 'E'
			print('Þú ert mjög áhættufælin eða getur ómögulega tekið áhættu og því mælum við með:')
		return Notandi
	Bool=True
	counter = 0
	while Bool==True:
		answer1 = str.lower(input("""Spurning 1: Laun og/eða heildargróði eru líkleg til að vaxa verulega á næstu árum.
			a: Mjög ósammála.
			b: Ósammála.
			c: Hvorki sammála né ósammála.
			d: Sammála.
			e: Mjög sammála.
			Svar: """))
		counter,Bool = getAnswer(answer1, counter)
	Bool=True
	while Bool==True:
		answer2 = str.lower(input("""Spurning 2: Ef ég væri að ákveða hvernig ég myndi ráðstafa eftirlaunum mínum, myndi ég velja fjárfestingu sem býður upp á fasta ávöxtun og stöðuleika.
			a: Mjög sammála.
			b: Sammála.
			c: Hvorki sammála né ósammála.
			d: Ósammála.
			e: Mjög ósammála.
			Svar: """))
		counter,Bool = getAnswer(answer2, counter)
	Bool=True
	while Bool==True:
		answer3 = str.lower(input("""Spurning 3: Ég trúi því að það að fjárfesta á hlutabréfamarkaðnum í dag sé eins og spilavíti - líkurnar eru á móti þér.
			a: Mjög sammála.
			b: Sammála.
			c: Hvorki sammála né ósammála.
			d: Ósammála.
			e: Mjög ósammála.
			Svar: """))
		counter,Bool  = getAnswer(answer3, counter)
	Bool=True
	while Bool==True:
		answer4 = str.lower(input("""Spurning 4: Ef ég væri að velja hlutabréf til þess að fjárfesta í, myndi ég leita að fyrirtækjum sem væru að framleiða vinsælar vörur framtíðinnar, eins og t.d. næsta pensillínið.
			a: Mjög ósammála.
			b: Ósammála.
			c: Hvorki sammála né ósammála.
			d: Sammála.
			e: Mjög sammála.
			Svar: """))
		counter,Bool = getAnswer(answer4, counter)
	Bool=True
	while Bool==True:
		answer5 = str.lower(input("""Spurning 5: Ef ég væri að fjárfesta með sparifé barna minna, myndi ég velja:
			a: Leggja inn á bankabók.
			b: Ríkisskuldabréf.
			c: Hlutabréfasjóð.
			d: Hlutabréf.
			e: Framvirka samninga.
			Svar: """))
		counter,Bool = getAnswer(answer5, counter)
	Bool=True
	while Bool==True:
		answer6 = str.lower(input("""Spurning 6: Fjárhagsleg velferð þessara fjölda manneskja veltur á mér.
			a: Fjórir eða meira.
			b: Þrír.
			c: Tveir.
			d: Einn.
			e: Aðeins mér einum.
			Svar: """))
		counter,Bool  = getAnswer(answer6, counter)
	Bool=True
	while Bool==True:
		answer7 = str.lower(input("""Spurning 7: Fjöldi ára þangað til ég býst við að hætta á vinnumarkaðnum:
			a: Hættur nú þegar.
			b: Minna en 5 ár.
			c: 5-14 ár.
			d: 15-24 ár.
			e: 25 eða meira.
			Svar: """))
		counter,Bool = getAnswer(answer7, counter)
	Bool=True
	while Bool==True:
		answer8 = str.lower(input("""Spurning 8: Mitt heildarverðmæti (verðmæti allra eigna umfram skuldir) er:
			a: Undir 2 milljón kr.
			b: 2 - 6.5 milljón kr.
			c: 6.5 - 20 milljón kr.
			d: 20 - 45 milljón kr.
			e: Yfir 45 milljónir.
			Svar: """))
		counter,Bool = getAnswer(answer8, counter)
	Bool=True
	while Bool==True:
		answer9 = str.lower(input("""Spurning 9: Sú upphæð sem ég hef sparað fyrir neyðartilvik, eins og brottvísun úr starfi eða óvæntur sjúkrakostnaður, hljóðar upp á:
			a: Eins mánaðar laun eða minna.
			b: Tvo til sex mánaða laun.
			c: Sjö mánaða til árs launa.
			d: Eins til tveggja ára launa.
			e: Meira en tveggja ára launa.
			Svar: """))
		counter,Bool = getAnswer(answer9, counter)
	Bool=True
	while Bool==True:
		answer10 = str.lower(input("""Spurning 10: Ég myndi frekar fjárfesta í hlutabréfasjóði en stökum hlutabréfum því hlutabréfasjóðir bjóða upp á faglega stjórnun og fjölbreytni.
			a: Mjög sammála.
			b: Sammála.
			c: Hvorki sammála né ósammála.
			d: Ósammála.
			e: Mjög ósammála.
			Svar: """))
		counter,Bool = getAnswer(answer10, counter)
	Bool=True
	while Bool==True:
		answer11 = str.lower(input("""Spurning 11: Mig langar/þarf að minnka heildarskuldir mínar.
			a: Mjög sammála.
			b: Sammála.
			c: Hvorki sammála né ósammála.
			d: Ósammála.
			e: Mjög ósammála.
			Svar: """))
		counter,Bool  = getAnswer(answer11, counter)
	Bool=True
	while Bool==True:
		answer12 = str.lower(input("""Spurning 12: Þegar ég fjárfesti, er ég tilbúinn til að sætta mig við lægri ávöxtun ef hún inniheldur enga áhættu, frekar en meiri ávöxtun með meiri áhættu.
			a: Mjög sammála.
			b: Sammála.
			c: Hvorki sammála né ósammála.
			d: Ósammála.
			e: Mjög ósammála.
			Svar: """))
		counter,Bool  = getAnswer(answer12, counter)
	Notandi = nidurstada(counter)
	#print('Þú ert í flokki %s' % Notandi)
	return Notandi

