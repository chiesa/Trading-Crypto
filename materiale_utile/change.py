################################SELL&BUY##############################
import krakenex
import json
import time
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')

from materiale_utile.variabili import T, P, MON1, MON2, mon1, mon2, mon1_min, mon2_min, change1_k, sig1_k, method1_k, change2_k, sig2_k, method2_k, change1_g, change2_g, wallet1_g, wallet2_g, wallet1_k, wallet2_k
from materiale_utile.valore_k import val
from materiale_utile.gestione_errori import gestione

val_kra = val()
g = gestione()

class change():

	#######buy_xrp_da_usd_gate
	#
	#
	def buy_xrp_da_usd_gate():
		conto = g.gestione(wait_gate_usdt(0.01))

		cancella = g.gestione(operazione_buy_gate(conto,change1_g))
		print(cancella)
		g.gestione(wait_buy_gate(change1_g,cancella,conto))

	#######buy_xrp_da_usd_gate
	#
	#TODO: test
	def buy_xrp_da_usd_gate1(object,val):
		g.gestione(wait_gate_usdt(float(val)))

		cancella = g.gestione(operazione_buy_gate(val,change1_g))

		g.gestione(wait_buy_gate1(val,change1_g,cancella))#CONTROLLARE CORRETTEZZA DEI PARAMETRI


	#######buy_xlm_da_usd_gate
	#
	#
	def buy_xlm_da_usd_gate():
		conto = g.gestione(wait_gate_usdt(0.01))

		cancella = g.gestione(operazione_buy_gate(conto,change2_g))

		g.gestione(wait_buy_gate(change2_g,cancella,conto))


	#######buy_xlm_da_usd_gate
	#
	# funzione con 1 parametro e ritorna la quantita di valuta cambiata:
	def buy_xlm_da_usd_gate(val):
		g.gestione(wait_gate_usdt(float(val)))

		cancella = g.gestione(operazione_buy_gate(val,change2_g))

		g.gestione(wait_buy_gate1(val,change2_g,cancella))

	#######buy_xrp_da_usd_kraken:
	#
	# permette l'acquisto dei xpl partendo da usd su kraken
	def buy_xrp_da_usd_kraken():
		g.gestione(wait_kraken_A('ZUSD',0.01))

		cancella = g.gestione(operazione_buy_kraken(change1_k,sig1_k))

		print(cancella)
		g.gestione(wait_buy_kraken(cancella,sig1_k,change1_g))


	#######buy_xrp_da_usd_kraken:
	#
	# permette l'acquisto dei xpl partendo da usd su kraken
	# NOTE: TEST utile per il futuro ma rivedere bene soprattutto condizione del while
	'''
	def buy_xrp_da_usd_kraken( val):
		wait_kraken_A('ZUSD', val)

		bilancioK=k.query_private('Balance')['result'] # VERIFICARE o recuperabile tramite responde
		RBX = val_kra.val_kra(change1_k)
		RUK_ASK = float(RBX['result'][sig1_k]['asks'][0][0])
		conto = str(float(bilancioK['ZUSD'])/RUK_ASK)

		cancella = k.query_private('AddOrder',
							 {'pair': change1_k,
							 'type': 'buy',
							 'ordertype': 'limit',
							 'price': str(RUK_ASK),
							 'volume': val})

		i=0

		while float(k.query_private('Balance')['result']['ZUSD'])-float(val):
			time.sleep(T)
			if i>0 and float(k.query_private('Balance')['result']['ZUSD'])-float(val):
				k.query_private('CancelOrder', {'txid':cancella['txif']})
				bilancioK=k.query_private('Balance')['result'] # VERIFICARE o recuperabile tramite responde
				RBX = val_kra.val_kra(change1_k)
				RUK_ASK = float(RBX['result'][sig1_k]['asks'][0][0])
				conto = str(float(bilancioK['ZUSD'])/RUK_ASK)
				cancella = k.query_private('AddOrder',
									 {'pair': change1_k,
									 'type': 'buy',
									 'ordertype': 'limit',
									 'price': str(RUK_ASK),
									 'volume': val})

			i = i+1
		'''


	#######buy_xlm_da_usd_kraken:
	#
	# permette l'acquisto dei xlm dai usd su kraken
	def buy_xlm_da_usd_kraken():
		g.gestione(wait_kraken_A('ZUSD',0.01))

		cancella = g.gestione(operazione_buy_kraken(change2_k,sig2_k))

		g.gestione(wait_buy_kraken(cancella,sig2_k,change2_g))

	#######sell_xrp_in_usd_kraken
	#
	#converto XRP in USD su kraken
	def sell_xrp_in_usd_kraken():
		# cicla finche non arrivano gli XRP su kraken
		g.gestione(wait_kraken_A(MON1,0.01))

		g.gestione(operazione_sell_kraken(change1_k,MON1))

		#attendo che avvengo il cambio
		g.gestione(wait_kraken_B(MON1,0.01))


	#######sell_xlm_in_usd_kraken
	#
	#
	#TODO:TEST
	def sell_xlm_in_usd_kraken():

		g.gestione(wait_kraken_A(MON2,0.01))

		g.gestione(operazione_sell_kraken(change2_k,MON2))

		g.gestione(wait_kraken_B(MON1,0.01))


	#######sell_xrp_in_usd_gate:
	#
	# vendita dei ripple per acquistare i usd su gate
	def sell_xrp_in_usd_gate():
		conto = g.gestione(wait_gate(mon1,0.01))

		cancella = g.gestione(operazione_sell_gate(conto,change1_g))
		print(cancella)
		g.gestione(wait_sell_gate(change1_g,mon1,cancella,conto))


	#######sell_xlm_in_usd_gate
	#
	#
	def sell_xlm_in_usd_gate():
		conto = g.gestione(wait_gate(mon2,0.01))

		cancella = g.gestione(operazione_sell_gate(conto,change2_g))

		g.gestione(wait_sell_gate(change2_g,mon2,cancella,conto))


def wait_gate(mon, val):
	data = gate.balances()
	bilancioG=json.loads(data)
	conto = bilancioG['available'][mon]
	while float(conto)<val:
		data = gate.balances()
		bilancioG=json.loads(data)
		conto = bilancioG['available'][mon]
	return conto

def wait_gate_usdt(val):
	data = gate.balances()
	bilancioG=json.loads(data)
	conto = bilancioG['available']['USDT']
	while float(conto)<float(val):
		data = gate.balances()
		bilancioG=json.loads(data)
		conto = bilancioG['available']['USDT']
	return conto

def wait_kraken_A(mon, val):
	while float(k.query_private('Balance')['result'][mon]) < val:
		time.sleep(T)

def wait_kraken_B(mon, val):
	while float(k.query_private('Balance')['result'][mon]) > val:
		time.sleep(T)

def operazione_buy_gate(conto, change):
	G = gate.orderBook(change)
	G_ASK = G['asks'][len(G['asks'])-1][0]
	cancella = gate.buy(change1_g, G_ASK, str(float(conto)/G_ASK))
	return cancella

def operazione_sell_gate(conto, change):
	G = gate.orderBook(change)#xrpUsdGate
	G_BID = G['bids'][0][0] #xrpUsdGate_bid
	cancella = gate.sell(change, G_BID, conto)
	return cancella

def wait_buy_gate(change,cancella,conto):
	data = gate.balances()
	bilancioG=json.loads(data)
	i = 0
	while float(bilancioG['locked']['USDT']) > 10:
		time.sleep(T)
		data = gate.balances()
		bilancioG=json.loads(data)
		if i>0 and float(bilancioG['locked']['USDT']) >= 10:
			conto = bilancioG['locked']['USDT']
			G = gate.orderBook(change)
			G_ASK = G['asks'][len(G['asks'])-1][0]
			try:
				cancella = json.loads(cancella)['orderNumber']
				gate.cancelOrder(cancella,change)
				cancella = gate.buy(change, G_ASK, str(float(conto)/G_ASK))
			except KeyError:
				raise
		else:
			return
		i = i+1

def wait_buy_gate1(val,change,cancella):
	data = gate.balances()
	bilancioG1=json.loads(data)
	time.sleep(T)
	i = 0
	print(bilancioG1)
	while float(bilancioG1['locked']['USDT']) > 10:
		time.sleep(T)
		data = gate.balances()
		bilancioG1=json.loads(data)
		if 'locked' in bilancioG1:
			if i>0 and float(bilancioG1['locked']['USDT']) >= 10:
				G = gate.orderBook(change)
				G_ASK = G['asks'][len(G['asks'])-1][0]
				cancella = json.loads(cancella)
				try:
					gate.cancelOrder(cancella['orderNumber'],change)
					cancella = gate.buy(change, G_ASK, str(float(bilancioG1['locked']['USDT'])/G_ASK))
					print(float(bilancioG1['locked']['USDT']))
				except KeyError:
					raise
				print(cancella)
		else:
			return
		i = i+1

def wait_sell_gate(change,mon,cancella,conto):
	data = gate.balances()
	bilancioG=json.loads(data)
	i = 0
	while float(bilancioG['available'][mon])>0.01:
		time.sleep(T)
		data = gate.balances()
		bilancioG1=json.loads(data)
		if 'locked' in bilancioG1:
			if i>0 and float(bilancioG['available'][mon])>0.01:
				data = gate.balances()
				bilancioG=json.loads(data)
				G = gate.orderBook(change)#xrpUsdGate
				G_BID = G['bids'][0][0]
				try:
					cancella = json.loads(cancella)
					gate.cancelOrder(cancella['orderNumber'],change)
					cancella = gate.sell(change, G_BID , bilancioG['available'][mon])
				except KeyError:
					raise
				print(cancella)
		else:
			return
			i=1+1

def wait_buy_kraken(cancella,sig,change):
	i=0
	while float(k.query_private('Balance')['result']['ZUSD']) > 0.01:
		time.sleep(T)
		if i>0 and float(k.query_private('Balance')['result']['ZUSD']) > 0.01:
			k.query_private('CancelOrder', {'txid':cancella['result']['txid'][0]})
			bilancioK=k.query_private('Balance')['result'] # VERIFICARE o recuperabile tramite responde
			K = val_kra.val_kra(change)
			K_ASK = float(K['result'][sig]['asks'][0][0])
			conto = str(float(bilancioK['ZUSD'])/K_ASK)
			cancella = k.query_private('AddOrder',
								 {'pair': change,
								 'type': 'buy',
								 'ordertype': 'limit',
								 'price': str(K_ASK),
								 'volume': conto})
		i = i+1

def operazione_buy_kraken(change,sig):
	bilancioK=k.query_private('Balance')['result']
	K = val_kra.val_kra(change)
	print(K)
	print(bilancioK)
	K_ASK = float(K['result'][sig]['asks'][0][0])
	conto = str((float(bilancioK['ZUSD'])/K_ASK))
	print(K_ASK)
	print(conto)
	print(float(conto)*K_ASK)
	cancella = k.query_private('AddOrder',
						 {'pair': change,
						 'type': 'buy',
						 'ordertype': 'limit',
						 'price': str(K_ASK),
						 'volume': conto})
	print(cancella)
	return cancella

def operazione_sell_kraken(change,MON):
	bilancioK=k.query_private('Balance')['result'] # VERIFICARE o recuperabile tramite responde
	k.query_private('AddOrder',
					{'pair': change,
					 'type': 'sell',
					 'ordertype': 'market',
					 'volume': bilancioK[MON]})
