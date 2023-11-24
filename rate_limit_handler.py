import requests
import json 
import time 
import datetime


def wait_for_rate_limit_reset(remaining, resetTime):
    # Imposta l'URL per ottenere i dettagli del limite di richieste API dal servizio di GitHub.
    # endpoint = "https://api.github.com/rate_limit"
    # Esegue una richiesta GET all'endpoint del limite di richieste API di GitHub utilizzando la libreria requests. 
    # Il parametro headers contiene l'autorizzazione necessaria per accedere all'API di GitHub.
    # rate = requests.get(endpoint, headers=header)
    # Converte la risposta della richiesta in formato JSON per poter facilmente accedere ai dati contenuti.
    # rateData = json.loads(rate.text)
    # Ottiene il timestamp Unix che indica quando il limite di richieste API sarà ripristinato. 
    # Il numero di richieste rimanenti per lo slot time attuale
    # remaining = rateData['resources']['core']['remaining']
    # remaining = int(rate.headers['X-RateLimit-Remaining'])
    temp = int(remaining)
    # print(f"remaining requests : {remaining}")
    if temp == 0:
        # Questo valore rappresenta il tempo in cui il limite verrà resettato, consentendo nuovamente le richieste.
        # resetTime = rateData['resources']['core']['reset']
        # Ottiene l'istante attuale.
        ms = datetime.datetime.now()
        # Ottiene il timestamp Unix corrente.
        nowTs = int(time.mktime(ms.timetuple()))
        # Calcola la differenza tra il tempo di reset del limite di richieste e il tempo corrente.
        diffTime = int(resetTime) - nowTs
        # Verifica se diffTime è maggiore di zero, cioè se il tempo rimanente prima del reset del limite è positivo.
        if diffTime > 0:
            # Stampa un messaggio che avverte che il limite di richieste API è stato superato e indica il tempo rimanente prima del reset.
            print(f"Superato il limite di richieste API. Attendi {diffTime} secondi prima di continuare.")
            # Fa dormire il programma per diffTime secondi, quindi attende fino a quando
            # il limite di richieste API è stato resettato prima di continuare con le richieste successive.
            time.sleep(diffTime)
