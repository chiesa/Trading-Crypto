############################WHITDRAE#######################
import krakenex
import json
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')

from materiale_utile.variabili import T, P, MON1, MON2, mon1, mon2, mon1_min, mon2_min, change1_k, sig1_k, method1_k, change2_k, sig2_k, method2_k, change1_g, change2_g, wallet1_g, wallet2_g, wallet1_k, wallet2_k


class prelievo():
    ########invio_xrp_da_kraken_a_gate
    #
    #
    def invio_xrp_da_kraken_a_gate(self):
        bilancioK=k.query_private('Balance')['result']

        k.query_private('Withdraw',
                        {'asset': mon1,
                         'key': 'gate_ripple',
                         'amount': bilancioK[MON1]})


    ################################Withdraw
    ########invio_xrp_da_gate_a_kraken
    #
    def invio_xrp_da_gate_a_kraken(self):
    	data = gate.balances()
    	bilancioG=json.loads(data)

    	gate.withdraw(mon1_min, bilancioG['available'][mon1], wallet1_k)


    ########invio_xlm_da_kraken_a_gate
    #
    #TODO:TEST
    def invio_xlm_da_kraken_a_gate(self):
    	bilancioK=k.query_private('Balance')['result'] # VERIFICARE o recuperabile tramite responde

    	k.query_private('Withdraw',
    					{'asset': mon2,
    					 'key': 'gate_lumen',
    					 'amount': bilancioK[MON2]})



    #######invio_xlm_da_kraken_a_gate
    #
    # funzione che un parametro: non bisogna inviare tutto
    #NOTE: utile in futuro:
    def invio_xlm_da_kraken_a_gate1(self,val):
    	k.query_private('Withdraw',
    					{'asset': mon2,
    					 'key': 'gate_lumen',
    					 'amount': val})



    ########invio_xlm_da_gate_a_kraken
    #
    #
    def invio_xlm_da_gate_a_kraken(self):
        data = gate.balances()
        bilancioG=json.loads(data)
        o = gate.withdraw(mon2_min, bilancioG['available'][mon2], wallet2_k)

    ########invio_xlm_da_kraken_a_gate
    #
    # funzione che un parametro: non bisogna inviare tutto
    #NOTE TEST
    def invio_xlm_da_gate_a_kraken1(self,val):

        gate.withdraw(mon2_min, val, wallet2_k)
