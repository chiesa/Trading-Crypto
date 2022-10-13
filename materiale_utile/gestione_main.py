################################SELL&BUY##############################
import krakenex
import time
import socket
import ssl
import sys
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL
from materiale_utile.variabili import T, p, profondita
from materiale_utile.inizio import inizio

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')
profondita = profondita()
inizio = inizio()

########main:
def main():
	sys.setrecursionlimit(p) #definisce la profondita della ricorsione
	inizio.inizio()
	print('ok, Kraken')

class gestione():
		#ritorna un risultato se esiste(tendenzialmente no!)
	def gestione_main(object):
		try:
			main()
		except KeyboardInterrupt:
			#print("visto il continuo ripetersi di errori è stato possibile interrompere il programma.\n la funzione che causa errori è:\n       ",str(funzione),"\n")
			print("A PRESTO BELLO!\n\n")
			return 'fine'
		except KeyError as err:
		    print("error Key: ")
		    print(err)
		except RecursionError:
		    #TODO: COME IMPORTARE LA PROFONDITA?
		    #aumenta la profondita della ricorsione
		    p=p*2
		    sys.setrecursionlimit(p)
		    print("socket err1\n\n")
		except socket.timeout as err: #socket.timeout: _ssl.c:629: The handshake operation timed out non gestita. line 318 -> NO INTERNET
		    print('\n',err,'\n')
		    time.sleep(T*2)
		except ssl.SSLError as err: #prove to socket.timeout: The read operation timed out
		    handle_error(err)
		    print("socket err, soketTimeOUT\n\n")
		    time.sleep(T*2)
		except socket.gaierror as err:
		    print("socket err4\n\n")
		    print(err)
		    time.sleep(T*2)
		except IndexError as err:
			print(err)
		except:
		    print("\n\n errore nell'eseguire la funzione")
		    #print(funzione)
		    print("\n\n")
		    time.sleep(T*2)
