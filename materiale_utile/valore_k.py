import krakenex
import time

k = krakenex.API()
k.load_key('materiale_utile/kraken.key')
#######CAMBIO KRAKEN:
#restituisce il cambio tra 2 valute dato da kraken (passando in change il nome delle 2 valute)
class val():
	def val_kra(object,change):
		while True:
			cambio = k.query_public('Depth',
									{'pair': change,
			                  		 'count': '1'}) #XLMusdKraken
			if cambio['error']!=[] :
				time.sleep(T)
			else:
				break
		return cambio
