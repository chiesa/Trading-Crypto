#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
import json
import krakenex
import time
import datetime
import sys
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL
from materiale_utile.change import change
from materiale_utile.whitdraw import prelievo
from materiale_utile.valore_k import val
from materiale_utile.caso import casi
from materiale_utile.gestione_errori import gestione

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')
prelievo = prelievo()
cambio = change()
val_kra = val()
casi = casi()
g = gestione()

############################# Variabili generale: #######################################
from materiale_utile.variabili import T,  p, P, MON1, MON2, mon1, mon2, mon1_min, mon2_min, change1_k, sig1_k, method1_k, change2_k, sig2_k, method2_k, change1_g, change2_g, wallet1_g, wallet2_g, wallet1_k, wallet2_k, profondita

profondita = profondita()
####################TODO:
'''
operazione base, valori:
 percentuale: 3.187889812889806
casi: 3.187889812889806 2.6736814757079745 -0.1921493274773479
caso 1:
error Key:
'bid'
3.2130423486619946

currency=xrp
currency=xlm

( 2018-04-19 05:07:43.796766 ) INZIO OPERAZIONE:

operazione base, valori:
 percentuale: 3.2130423486619946
casi: 3.2130423486619946 2.925887535630991 -0.1921493274773479
caso 1:
error Key:
'bid'
'''
# c'è un ciclio infinito o in generale il programma va in loop
# --> se esiste un ordine perchè sono stati scambiati meno del 100% (ma maggiore al 90%) di un offerta bisognerà cancellarla <--
###########
# controllare variabili importate nel file caso.py
# ECCEZIONI (FATTO?): se si fa 1 offerta non bisogna poi deve o cancellarla portare a termine l'operazione, se il sito non risponde non posso uscrire e basta. (fatto)
# fare metodi con todo nelle classi whitdraw e change
# TEST: waitChage. -> fondamentale
# TEST: dei singoli pezzi di class change e whitdraw
# verificare che variabile p funzioni. <- controllare funzioni la gestione della profondita

# fatto vel:
	# variabile conto (non è sempre lo stesso varia ogni volta, dopo tutti i while va aggiornato)-> NON HO MAI IL VALORE IN USD, bisogna dividerla per il valore della valuta in ask,
	# controllare le condizioni dei while attenzione a quando è true e false per i cicli di wait e SEMPRE VALORE !=0 (fatto ma con < o > 0.01)
	# in while MON1 in k.query_private('Balance')['result'] cambiare il valore da stringa a float! (fatto)
	# controllare portafoglio kraken su cui invia gate (deve essere sempre lo stesso, fare un controllo) (fatto)
	# nel bilancio per le wait (ad esempio) su kraken USD è ZUSD. su gate USDT' e non usd!! (fatto)
	# attenzione nei k.query_private('Balance')['result'][MON1], nei withdraw mon1 (fatto)
	# VERIFICARE: verifica quando si usa sell e quando buy e modificarlo nel prog (fatto un primo controllo veloce)

# PER AVVIO:
	#modificare 3%, 5% e 75% nei valori ritenuti piu sensati, 1minuto è troppo per la wait (ora 30 sec) [occhio che sono in diversi file]
	# modificare print rendendole utili-> lasciare solo quando scatta: percentuali e se va a buon fine o no (fatto parzialmente)
# NOTE: "versioni successive" commenti che contengono passaggi da estendere (o parti commentati utili per espansioni, ecc)
	# quando kraken avrà usd per definire se ho avuto errori per chiamare la funzione cambio prima: if cancella['error'] == []

################################# funzione principale: ###########################################
class inizio():
	def inizio(object):
		####### NOTE migliorie:
		# vedere la quantita che è cambiabile e quindi valurare la cifra in dollari con cui fare la transazione
		# mettere usd anche su kraken -> aumentare le possibili evoluzioni del programma

		#aumentare dinamicamente la profondita ricorsiva per evitare: RecursionError
		global p
		global P
		P=P+5
		if P>=p:
			p=profondita.mod_p(p*p)
			print(p)
			sys.setrecursionlimit(p)
		#################################### RACCOLTA DATI: ####################################
		#
		# dati Kraken:
		RBX = val_kra.val_kra(change1_k) #xrpusdKraken
		LBX = val_kra.val_kra(change2_k) #xlmusdKraken
		# BUK = val_kra.val_kra('USDUSD') #usdUsdKraken <-SERVE NELLA VERSIONE SUCCESSIVE.

		# Valore xrp in usd su gate
		RUG = gate.orderBook(change1_g)#xrpUsdGate
		RUG_ASK = RUG['asks'][len(RUG['asks'])-1][0] #xrpUsdGate_ask
		RUG_BID = RUG['bids'][0][0] #xrpUsdGate_bid

		# Valore XLM in usd su gate
		LUG = gate.orderBook(change2_g) #xlmUsdGate
		LUG_ASK = LUG['asks'][len(LUG['asks'])-1][0] #xlmUsdGate_ask
		LUG_BID = LUG['bids'][0][0] #xlmUsdGate_bid

		# Valore usd in usd su gate
		# BUG = gate.orderBook(changeUB_g) #XLMUsdGate
		# BUG_ASK = BUG['asks'][len(BUG['asks'])-1][0] #XLMUsdGate_ask
		# BUG_BID = BUG['bids'][0][0] #XLMeUsdGate_bid


		# Valore xrp in usd su kraken
		RUK_ASK = float(RBX['result'][sig1_k]['asks'][0][0]) #* BUG_ASK
		RUK_BID = float(RBX['result'][sig1_k]['bids'][0][0]) #* BUG_ASK

		# Valore XLM in usd su kraken
		LUK_ASK = float(LBX['result'][sig2_k]['asks'][0][0]) #* BUG_ASK
		LUK_BID = float(LBX['result'][sig2_k]['bids'][0][0]) #* BUG_ASK


		########################## CONTI ###########################################
		#obiettivo: vedere quando lo scarto di xrp insieme a quello di XLM, supera col suo valore di acquisto, il valore di vendita di almeno il 5% dell'altro.
		#
		# voglio quindi: (1 sarà il sito con cambio più alto, minore quello di D2 (RIVEDERE ASK E BID)
		# 		percentuale_xrp: (D1(bid)-D2(ask)) *100 / D1(bid)
		# 		precentuale_XLM: (E1(bid)-E2(ask)) * 100 / E1(bid)
		# 		if		percentuale_xrp + percentuale_xlm > 5%
		# 			allora: prosegui
		# 			se no:  wait&reply.
		#
		perc_xrp_KG = cal_per(RUK_BID, RUG_ASK) #percentuale xrp da Kraken a Gate
		perc_xlm_KG = cal_per(LUK_BID, LUG_ASK) #percentuale xlm da Kraken a Gate
		perc_xrp_GK = cal_per(RUG_BID, RUK_ASK) #percentuale xrp da Gate a Kraken
		perc_xlm_GK = cal_per(LUG_BID, LUK_ASK) #percentuale xlm da Gate a Kraken
		# percentuale xrp sulle richieste/offerte, se maggiore di 5 si prova a fare un offerta sul situo se va a buon fine si procede con le transazioni
		#
		# MODIFICHE NOTE TOGLIERE: utile in versioni successive
		#perc_ASK_xrp_KG = cal_per(RUK_ASK, RUG_ASK) # ASK xrp K->G (offerta di acquisto) + XLM da G->K
		#perc_BID_xrp_KG = cal_per(RUK_BID, RUG_BID) # BID xrp K->G (offerta di vendita)+ XLM da G->K
		#perc_ASK_xlm_KG = cal_per(LUK_ASK, LUG_ASK) # ASK xlm K->G (offerta di acquisto)  + xrp da G->K
		#perc_BID_xlm_KG = cal_per(LUK_BID, LUG_BID) # BID xlm K->G (offerta di vendita) + xrp da G->K

        # SERVE IL PRIMO (commentato) NON IL SECONOD.. CONTROLLARE
		#cal_per(RUG_ASK, RUK_ASK) # ASK: xrp G->K (offerta di acquisto) + XLM da K->G
		perc_BID_xrp_GK = cal_per(RUK_BID, RUG_BID) # BID: xrp G->K (offerta di vendita) + xlm da K->G #NOTE modificato 25 APRILE: offerta va fatto ul minore
		perc_ASK_xlm_GK = cal_per(LUG_ASK, LUK_ASK) # ASK: xlm G->K (offerta di acquisto) + xrp da K->G
		perc_BID_xlm_GK = cal_per(LUK_BID, LUG_BID) # BID: xlm G->K (offerta di vendita) + xrp da K->G #NOTE modificato 25 APRILE: offerta va fatto ul minore

		#percentuale che rende acquisto xlm su kraken vendo su Gate (e quindi aquisto xrp su Gate e vendo su kraken)
		#NOTE: al mometo non si può acquistare su kraken xlm, non ho usd <- fare piu avanti: versioni successive
		#perc_KG = perc_xlm_KG + perc_xrp_GK;

		#percentuale che rende acquisto xlm su Gate vendo su kraken (e quindi aquisto xrp su kraken e vendo su Gate)
		perc_GK = perc_xrp_KG + perc_xlm_GK;

		########################## ALGORITMO ###########################################
		#
		#se una percentuale è maggiore del 5% allora effettua una determinata procedura, si può anche fare un tentativo se non supera il 5% (analizzato nell'algoritmo)
		#massimo che serve nel else: if:
		caso_max = max(perc_BID_xrp_GK, perc_ASK_xlm_GK, perc_BID_xlm_GK, abs(perc_ASK_xlm_GK))
		print('casi',perc_BID_xrp_GK, perc_ASK_xlm_GK, perc_BID_xlm_GK, abs(perc_ASK_xlm_GK))
		print(caso_max)

		"""
		# NOTE: caso base: usare quando si ha anche usd su KRAKEN
		#if (perc_KG > perc_GK) & (perc_KG>5):
		#	print("transazioni1!!")
		#	print(perc_KG)
		#elif (perc_GK < perc_KG) & (perc_GK>5):
		#	print("transazioni2!!")
		#	print(perc_GK)
		"""
		if (perc_GK>3 or caso_max > 3):
			data = gate.balances()
			bilancioG=json.loads(data)
			bilancioK=k.query_private('Balance')['result']

			# PORTAFOGLI: NOTE: si possono aumentare le prestazioni creano i portafoglio solo all'inizio o (MEGLIO) facendo le operazioni sotto solo quando strettamente necessarie per le transazioni che stanno per avvenire.
			KR = getWallet_K_xrp() #portafoglio di kraken per i ripple
			KL = getWallet_K_xlm() #portafoglio di kraken per i lumen

			GR = json.loads(gate.depositAddres("xrp"))['addr'].replace("/", " ") #portafoglio di gate per i ripple (sigla su kraken)
			GL = json.loads(gate.depositAddres("xlm"))['addr'].replace("/", " ") #portafoglio di gate per i lumen (sigla su kraken)

			if 'false' in bilancioG['result']:
				print("\n\n\n\nproblema result! non vanno più le chiavi di gate?? CONTROLLA!!\n\n\n\n")
				raise KeyboardInterrupt
			elif GR != wallet1_g or GL != wallet2_g:
				print('\n\n\n\nUn portafoglio salvato su kraken, non corrisponde a quello di ricezione di gate. MODIFICARE!!!!!\n\n\n\n')
				raise KeyboardInterrupt
			elif KR != wallet1_k or KL != wallet2_k:
				print('\n\n\n\nkraken ha modificato il portafoglio, primo invio da gate va fatto perforza a mano. MODIFICARE!!!!!\n\n\n\n')
				raise KeyboardInterrupt
			elif float(bilancioG['available']['USDT']) > 0.01:
				bil_UG = bilancioG['available']['USDT'] # problema se vendo tutti gli XRP sarà 0
				print("\n(",str(datetime.datetime.now()),") INZIO OPERAZIONE:\n")
			else:
				print("problema!")
				inizio()
			conto = bil_UG

		if perc_GK>3:
			print("operazione base, valori:\n percentuale:", perc_GK)

			#acquisto XLM su gate, funzione con paramentro, ritorna la quantita di valuta acquistata
			acquistata = cambio.buy_xlm_da_usd_gate(conto)
			#acquisto su kraken usd
			cambio.sell_xlm_in_usd_kraken()
			#acquisto su kraken xrp
			cambio.buy_xrp_da_usd_kraken()
			#invio XRP kraken -> gate
			prelievo.invio_xrp_da_kraken_a_gate()
			# cambio xrp in USDT
			cambio.sell_xrp_in_usd_gate()
			#invio XLM gate-kraken
			prelievo.invio_xlm_da_gate_a_kraken(acquista)

			# cicla finche non arrivano gli xlm su kraken
			while float(k.query_private('Balance')['result'][MON2]) < 0.01:
				time.sleep(T)

			print('FINE OPERAZIONE!')

		#ricerco il massimo tra i valori tutte le possibili combinazioni di acquisto e vendita, se la sua percentuale è maggiore di 5. cerca qual'è e di conseguenza effetto le transizioni, altrimenti rinizio.
		elif caso_max > 3: #TODO modificare 3
			print("operazione base, valori:\n percentuale:", caso_max)
			print('casi:',perc_BID_xlm_GK,perc_ASK_xlm_GK,perc_BID_xrp_GK)
			#CASO 1:
			if caso_max == perc_BID_xlm_GK :
				# Metto un offerta da USDT a XLM, se va a buon fine:
					# su kraken faccio: xlm->usd->xrp
					# invio xrp a gate
					# converto xrp in usd
					# invio i xlm che ho comprato a kraken
				print("caso 1: ") #print di controllo poi toglierle

				# procedura:
				if float(conto)>(float(bilancioG['available'][mon2])*LUG_BID):
					conto = str(float(bilancioG['available'][mon2])*LUG_BID)

				LUG = gate.orderBook(change2_g)
				LUG_BID = LUG['bids'][0][0]

				n_order = gate.buy(change2_g, LUG_BID, str(float(conto)/LUG_BID))

				if json.loads(n_order)['result'] == 'true':
					g.gestione(casi.caso1(conto, n_order, bilancioG, LUG_BID))

			#NOTE:
			#elif caso_max == perc_BID_xrp_GK :
			#	print("caso 0: ") #print di controllo poi toglierle
				#OPZIONE:
				#
				#
				# metto un offerta per xrp su GATE in BID se va a buon fine chiamo la una funzione che fa cambia su gate XLM->USD, da kraken XLM invia su gate, quando arrivano i xrp gli cambia

			#CASO 2
			elif caso_max == perc_ASK_xlm_GK :
				# si mette un offerta di vendita(ask) di lumen su kraken, se va a buonfine
					# compro xrp con i soldi ricavati dalla vendita dei lumen
					# invio xrp da gate a kraken
					# vedo saldo_kraken (uso alla fine per far whitdraw del numero corretto di xlm da kraken)
					# cambio: xrp->usd->xlm
					# invio xlm che gia erano presenti su kraken a gate

				print("caso 2: ") #print di controllo poi toglierle
				print(caso_max)

				if(float(conto) > float(bilancioG['available'][mon2])*LUG_ASK):
				    conto = str(float(bilancioG['available'][mon2]))

				print(conto)
				n_order = gate.sell(change2_g, LUG_ASK, conto[:6])
				print(n_order)
				if json.loads(n_order)['result'] == 'true':
					g.gestione(casi.caso2(conto, n_order, LUG_ASK, RUG_BID, bilancioG))


			#caso 3:
			elif caso_max ==  perc_BID_xrp_GK:
				#OPZIONE:
				#
				# metto un offerta per xrp su GATE in ASK, se va a buon fine:
				 	# cambia su gate XLM->USD
					# da kraken XLM invia su gate
					# quando arrivano i XRP su kraken XRP->USD->XLM

				print("caso 3: ") #print di controllo poi toglierle
				if(float(conto) > float(bilancioG['available'][mon1])*RUG_BID):
				    conto = str(float(bilancioG['available'][mon1])*RUG_BID)

				n_order = gate.buy(change1_g, RUG_BID, str(float(conto)/RUG_BID))

				if json.loads(n_order)['result'] == 'true':
					g.gestione(casi.caso3(conto, n_order, bilancioG))

			elif caso_max == abs(perc_ASK_xlm_GK):
				print("caso 4:")
				if(float(conto) > float(bilancioK[MON2])*LUK_BID):
				    conto = str(float(bilancioK[MON2])*LUK_BID)

				n_order = k.query_private('AddOrder',
									 {'pair': change2_k,
									 'type': 'sell',
									 'ordertype': 'limit',
									 'price': LUK_BID,
									 'volume': str(float(conto)/LUK_BID)})

				print(n_order)
				if n_order['error'] == []:
					g.gestione(casi.caso4(conto, n_order, bilancioK, bilancioG))


			print('FINE OPERAZIONE!')

		#time.sleep(T)
		inizio()


#######PROCEDURA: NOTE: si puo generalizzare??

####### getWallet_K, getWallet_K_xrp, getWallet_K_xlm:
#
# restituisce il portafoglio di kraken corrisponedente alla valuta e al metodo.
# se il portafoglio dovesse non essere esistente lo crea e lo restituisce come stringa
def getWallet_K(mon, meth):
	wal=k.query_private('DepositAddresses',
	             		{'asset':mon,
	          		 	'method': meth})
	if wal['result']==[]:
		wal = k.query_private('DepositAddresses',
		            		{'asset':mon,
		              	 	'method': meth,
						 	'new':'true'})
	# NOTE: MOLTO IMPORTANTE: QUESTO PROCEDIMENTO VALE SOLO PER LUMEN/RIPPLE CHE NECESSITA DI TAG altrimenti si può togliere l'ultima parte:
	return wal['result'][0]['address']+' '+str(wal['result'][0]['tag'])

# sfruttano getWallet_K per creare i portafoglio specifici di xlm e xrp (NON RICHIEDONO PARAMENTRI)
def getWallet_K_xrp():
	return getWallet_K(MON1,method1_k)
def getWallet_K_xlm():

	return getWallet_K(MON2,method2_k)
#######CALCOLO PERCENTUALE:
#
#
def cal_per(A, B):
	per = (A-B)*100/A
	return per

#######POSSIBILE SCATTO CON ATTESA:
#
# se il prezzo o vendita sui 2 siti ha uno scarto del 5% mi metto in attesa, metto un ordine se dopo 1 minuto e trenta ho venduto allora faccio le transazioni
def poss(A, B, C):
	per = ( (A-B)*100/A ) + C
	return per
