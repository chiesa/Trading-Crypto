################################SELL&BUY##############################
import krakenex
import time
import socket
import ssl
import sys
from gateex.gateAPI import GateIO
from materiale_utile.gate_key import apikey, secretkey, API_URL
from materiale_utile.variabili import T, p, profondita

gate = GateIO(API_URL,apikey,secretkey)
k = krakenex.API()
k.load_key('materiale_utile/kraken.key')
profondita = profondita()

class gestione():
    #ritorna un risultato se esiste(tendenzialmente no!)
    def gestione(self,funzione):
        i=0
        while True:
            i = i+1
            try:
                risultato = funzione
                return risultato
                time.sleep(T)
            except KeyboardInterrupt:
                if i>=10:
                    print("visto il continuo ripetersi di errori è stato possibile interrompere il programma.\n") #la funzione che causa errori è:\n       ",funzione,"\n")
                    print("A PRESTO BELLO!\n\n")
                    return None
                else:
                    print(i)
                    print("non è possibile interrompere il programma perchè è nel mezzo di un operazione.")
            except KeyError as err:
                print("error Key: ")
                print(err)
            except RecursionError:
                #TODO: COME IMPORTARE LA PROFONDITA?
                #aumenta la profondita della ricorsione
                p=profondita.mod_p(p*2)
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
            except:
                print("\n\n errore nell'eseguire la funzione")
                #print(funzione)
                print("\n\n")
                time.sleep(T*2)
        return risultato
