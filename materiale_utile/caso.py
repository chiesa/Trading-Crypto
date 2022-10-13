import krakenex
import json
import time
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL
from materiale_utile.change import change
from materiale_utile.whitdraw import prelievo

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')
cambio = change()
prelievo = prelievo()

############################# Variabili generale: #######################################
from materiale_utile.variabili import T,  p, P, MON1, MON2, mon1, mon2, mon1_min, mon2_min, change1_k, sig1_k, method1_k, change2_k, sig2_k, method2_k, change1_g, change2_g, wallet1_g, wallet2_g, wallet1_k, wallet2_k, profondita


class casi():

    def caso1(object, conto, n_order, bilancioG, LUG_BID):
        soldi_scambiati = waitChage(float(conto[:6]), conto[:6], 'USDT')

        print("caso 1: ")

        data = gate.balances()
        bilancioG1=json.loads(data)

        if float(soldi_scambiati)/float(conto)*100>=90 or float(soldi_scambiati)==float(conto):
            #vendo xlm su kraken
            cambio.sell_xlm_in_usd_kraken()
            #compro ripple su kraken
            cambio.buy_xrp_da_usd_kraken()
            #invio i xrp da kraken a gate
            prelievo.invio_xrp_da_kraken_a_gate()
            # vendita dei ripple per acquistare i usd su gate
            cambio.sell_xrp_in_usd_gate()
            #invio i xlm scambiati a kraken
            soldi_scambiati = str(float(soldi_scambiati)/LUG_BID)
            prelievo.invio_xlm_da_gate_a_kraken(soldi_scambiati)
        else:
            #torno indietro
            print("\nTORNO INDIETRO, LA TRANSAZIONE NON HA AVUTO SUCCESSO. HO CAMBIATO IL ", soldi_scambiati," su ",conto,". cioè il", str(float(soldi_scambiati)/float(conto)*100))
            # Cancella ordine:
            #
            # risultato:
            #		{
            #		"result":"true",
            #		"msg":"Success"
            #		}
            # NOTE: si potrebbe controllare che abbia successo
            # cancello l'ordine

            n_order = json.loads(n_order)['orderNumber']
            gate.cancelOrder(n_order,change2_g)


            # Valore XLM in usd su gate
            LUG = gate.orderBook(change2_g) #XLMUsdGate
            LUG_BID = LUG['bids'][0][0] #XLMeUsdGate_bid
            data = gate.balances()
            bilancioG1=json.loads(data)
            #vendo i soldi che gia ho comprato

            gate.sell(change2_g, LUG_BID, str(float(bilancioG1['available'][mon2]) - float(bilancioG['available'][mon2])))

    def caso2(object, conto, n_order, LUG_ASK, RUG_BID, bilancioG):
        soldi_scambiati = waitChage(float(conto[:6]), bilancioG['available'][mon2], mon2)

        data = gate.balances()
        bilancioG1=json.loads(data)
        #se è piu del 90% effettuiamo lo scambio, altrimenti no
        if float(conto[:6])*90/100<=soldi_scambiati:

            print(soldi_scambiati)
            #vedo il saldo di xlm su kraken
            saldo_kraken_xlm = k.query_private('Balance')['result'][MON2]
            #cambio usd in ripple(usd acquistati tramite la vendita di xlm)
            soldi_scambiati = str(float(soldi_scambiati)/LUG_ASK)
            cambio.buy_xrp_da_usd_gate1(soldi_scambiati)
            #invio xrp da gate a kraken
            prelievo.invio_xrp_da_gate_a_kraken()
            # vendita dei ripple per acquistare i usd su gate
            cambio.sell_xrp_in_usd_gate()
            # acquisto i lumen su kraken
            cambio.buy_xlm_da_usd_kraken()
            #invio saldo_kraken_xlm a gate
            prelievo.invio_xlm_da_gate_a_kraken(saldo_kraken_xlm)
        else:
            #torno indietro
            print("\nTORNO INDIETRO, LA TRANSAZIONE NON HA AVUTO SUCCESSO. HO CAMBIATO IL ", soldi_scambiati," su ",conto,". cioè il", str(float(soldi_scambiati)/float(conto)*100))

            # Cancella ordine:
            #
            # risultato:
            #		{
            #		"result":"true",
            #		"msg":"Success"
            #		}
            # NOTE: si potrebbe controllare che abbia successo
            #cancello l'ordine

            n_order = json.loads(n_order)['orderNumber']
            print(n_order)
            gate.cancelOrder(n_order,change2_g)

            #Valore XLM in usd su gate
            LUG = gate.orderBook(change2_g) #XRPUsdGate
            LUG_BID = LUG['bids'][0][0] #XRPeUsdGate_bid
            data = gate.balances()
            bilancioG1=json.loads(data)

            # torno indietro
            gate.buy(change2_g, LUG_BID, str(float(bilancioG1['available']['USDT'])-float(bilancioG['available']['USDT'])/LUG_BID))

    def caso3(object, conto, n_order, bilancioG):
        soldi_scambiati = waitChage(float(conto), conto, 'USDT')
        #se ho cambiato piu del 90% dei soldi vado avanti altrimenti torno indietro
        if float(soldi_scambiati)/float(conto)*100>=90 or float(soldi_scambiati)==float(conto):

        	#acquisto i dollari dai XLM
        	cambio.sell_xlm_in_usd_kraken()
        	#invio i ripple da gate a kraken
        	prelievo.invio_xrp_da_gate_a_kraken()
        	# vendo i ripple su kraken
        	cambio.sell_xrp_da_usd_kraken()
        	#invio i lumen da kraken a gate
        	prelievo.invio_xlm_da_kraken_a_gate()
        	# acquisto i lumen su kraken
        	cambio.buy_xlm_da_usd_kraken()
        else:
            #torno indietro

        	print("\nTORNO INDIETRO, LA TRANSAZIONE NON HA AVUTO SUCCESSO. HO CAMBIATO IL ", soldi_scambiati," su ",conto,". cioè il", str(float(soldi_scambiati)/float(conto)*100))

        	# Cancella ordine:
        	#
        	# risultato:
        	#		{
        	#		"result":"true",
        	#		"msg":"Success"
        	#		}
        	# NOTE: si potrebbe controllare che abbia successo

        	n_order =json.loads(n_order)['orderNumber']
        	gate.cancelOrder(n_order,change1_g)


        	# Valore XRP in usd su gate
        	LUG = gate.orderBook(change1_g) #XRPUsdGate
        	LUG_BID = LUG['bids'][0][0] #XRPeUsdGate_bid
        	data = gate.balances()
        	bilancioG=json.loads(data)

        	gate.sell(change1_g, RUG_BID, bilancioG['available'][mon1])

    def caso4(object, conto, n_order, bilancioK, bilancioG):
        soldi_scambiati = waitChage_k(float(conto), bilancioK['ZUSD'], 'ZUSD')
        if float(soldi_scambiati)/float(conto)*100>=90 or float(soldi_scambiati)==float(conto):
            saldo_xlm = bilancioG['available'][mon2]
            #acquisto XLM da dollari
            cambio.buy_xlm_da_usd_gate()
            #cambio usd in ripple(usd acquistati tramite la vendita di xlm)
            cambio.buy_xrp_da_usd_kraken()
            #invio i ripple da kraken a gate
            prelievo.invio_xrp_da_kraken_a_gate()
            # vendo i ripple su kraken
            cambio.sell_xrp_da_usd_gate()
            #invio i lumen da kraken a gate
            prelievo.invio_xlm_da_gate_a_kraken1(saldo_xlm)

        else:
            #torno indietro
            print("\nTORNO INDIETRO, LA TRANSAZIONE NON HA AVUTO SUCCESSO. HO CAMBIATO IL ", soldi_scambiati," su ",conto,". cioè il", str(float(soldi_scambiati)/float(conto)*100))

            k.query_private('CancelOrder', {'txid':n_order['result']['txid'][0]})
            if float(k.query_private('Balance')['result']['ZUSD'])>0.01 :
                cambio.buy_xlm_da_usd_kraken()

####### waitChage VALE SOLO SU GATE:
#
#
# dal la possibilità di inserire un offerta e aspettare tot tempo per verificare
# se si ha scambiato piu del 90% allora si considera sia andato a buon fine
# e si effettua lo scambio altrimenti si aspetta di scambiare abbastastanza, se non si arriva al 90% si torna indietro.
def waitChage(soldi_da_scambiare, bilancio_vecchio, t_val):
    print('ARRIVO')
    soldi_scambiati = 0
    ciclo=0
    print(soldi_scambiati)
    while soldi_da_scambiare*90/100>=soldi_scambiati:
        print('entro')
        if ciclo==0:
            time.sleep(T)
        elif soldi_da_scambiare*90/100>=soldi_scambiati:
        	time.sleep(T)
        ciclo = ciclo + 1
        data = gate.balances()
        bilancio_nuovo = json.loads(data)['locked'][t_val]
        print(bilancio_vecchio)
        print(bilancio_nuovo)
        if float(bilancio_vecchio)-float(bilancio_nuovo)==soldi_da_scambiare:
            print('1')
            print(soldi_scambiati)
            soldi_scambiati = soldi_da_scambiare
            break
            print(soldi_scambiati)
        else:
            print('2')
            print(float(bilancio_vecchio)-float(bilancio_nuovo))
            soldi_scambiati = float(bilancio_vecchio)-float(bilancio_nuovo)
        if ciclo == 10:
            break
    return float(soldi_scambiati)

def waitChage_k(soldi_da_scambiare, bilancio_vecchio, t_val):
    print('ARRIVO')
    soldi_scambiati=0
    ciclo=0
    while soldi_da_scambiare*90/100<=soldi_scambiati:
        print('entro')
        if ciclo==0:
            time.sleep(T)
        elif soldi_da_scambiare*90/100<=soldi_scambiati:
        	time.sleep(T)
        ciclo = ciclo + 1
        bilancio_nuovo = k.query_private('Balance')['result'][t_val]

        if float(bilancio_vecchio)-float(bilancio_nuovo)==soldi_da_scambiare:
        	soldi_scambiati = soldi_da_scambiare
        	break
        else:
            soldi_scambiati = float(bilancio_vecchio)-float(bilancio_nuovo)
        if ciclo == 10:
            return float(soldi_scambiati)
    return float(soldi_scambiati)
