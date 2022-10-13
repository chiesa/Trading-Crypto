#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# encoding: utf-8
import json
import krakenex
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL
from materiale_utile.whitdraw import prelievo
from materiale_utile.change import change
from materiale_utile.valore_k import val
from materiale_utile.valore_k import val
from materiale_utile.gestione_errori import gestione

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')
prelievo = prelievo()
cambio = change()
val_kra = val()
g = gestione()


############################# Variabili generale: #######################################
from materiale_utile.variabili import T, p, P, MON1, MON2, mon1, mon2, mon1_min, mon2_min, change1_k, sig1_k, method1_k, change2_k, sig2_k, method2_k, change1_g, change2_g, wallet1_g, wallet2_g, wallet1_k, wallet2_k



try:
    #change.sell_xlm_in_usd_gate()
    #change.buy_xlm_da_usd_gate()
    #prelievo.invio_xlm_da_gate_a_kraken()

    #NOTE: SALTATO PASSO VENDITA XLM
    #change.buy_xrp_da_usd_kraken()
    #prelievo.invio_xrp_da_kraken_a_gate()
    #change.sell_xrp_in_usd_gate()
    #change.buy_xrp_da_usd_gate()
    #prelievo.invio_xrp_da_gate_a_kraken()
    #change.sell_xrp_in_usd_kraken()
    #change.buy_xlm_da_usd_kraken()
    #change.buy_xlm_da_usd_kraken()
    #prelievo.invio_xlm_da_kraken_a_gate1(100)

except KeyboardInterrupt:
    None
#print(g.gestione(k.query_private('Balance')['result']))
#cambio.sell_xlm_in_usd_gate()
#cambio.buy_xlm_da_usd_gate('2')
