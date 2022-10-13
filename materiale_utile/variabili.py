############################# Variabili generale: #######################################
T=20 #tempo d'attesa nei wait (in secondi)
p=100 #profondita della ricorsione
P=2 #conta quanto siamo in profondita partendo da due e permette l'incremento di p
# permettono cambiare i tipi di valuta nel programma:
#NOTE: esportare in un altro file per fare pulizia?? si accede al file, si modificano variabili senza dover accedere al programma vero??
MON1 = 'XXRP'#sigla valuta 1
MON2 = 'XXLM' #sigla valuta 2
mon1 = 'XRP'
mon2 = 'XLM'
mon1_min = 'xrp'# i withdraw di gate usano le sigle minuscole per il resto maiuscole
mon2_min = 'xlm'
change1_k = 'XRPUSD' #xrpusdKraken: val1->usd
sig1_k = 'XXRPZUSD' #sigla: val1->usd
method1_k = 'Ripple XRP' #metodo per per avere il wallet della val1
change2_k = 'XLMUSD' #xlmusdKraken: val2->usd
sig2_k = 'XXLMZUSD' #sigla: val2->usd
method2_k = 'Stellar XLM' #metodo per per avere il wallet della val2
change1_g = 'xrp_usdt' #xrpUsdGate: val1->usd
change2_g = 'xlm_usdt' #xlmUsdGate: val2->usd
wallet1_g = 'rHcFoo6a9qT5NHiVn1THQRhsEGcxtYCV4d 42923401'
wallet2_g = 'GBC6NRTTQLRCABQHIR5J4R4YDJWFWRAO4ZRQIM2SVI5GSIZ2HZ42RINW 42923401'
wallet1_k = 'rLHzPsX6oXkzU2qL12kHCH8G8cnZv1rBJh 1474092711'
wallet2_k = 'GA5XIGA5C7QTPTWXQHY6MCJRMTRZDOSHR6EFIBNDQTCQHG262N4GGKTM 2220523511'
#changeUB_g = 'usd_usdt' #XLMUsdGate: usd->usd

class profondita():
    def mod_p(object,val):
        p=val
        return p
