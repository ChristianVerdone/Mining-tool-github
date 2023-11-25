import requests
import json 
import time 
import datetime
import time
import mainTool



# Prima di chiamare il metodo dobbiamo tenere traccia delle richieste e del tempo 
# Provato con l'azione search_repo 
# sostituendo 900 con 3 richieste possibili al minuto e ponendo nel file .txt 8 repository 
#Passiamo il tempo di inizio e il numero di richieste fino a quel momento
def rate_minute():
    start_time = mainTool.start_time
    request_count= mainTool.requests_count

    #tempo corrente
    current_time = time.time()
    # Calcola il tempo trascorso dall'inizio del periodo
    elapsed_time = current_time - start_time  
    if elapsed_time > 60 & request_count < 900:
        # Se è passato più di un minuto, resetta il conteggio delle richieste e il tempo di inizio
        mainTool.start_time = time.time()
        mainTool.requests_count = 0
    elif elapsed_time <= 60 & request_count > 900:
        # Stampa un messaggio che avverte che il limite di richieste API è stato superato e indica il tempo rimanente prima del reset.
        print(f"Superato il limite di richieste API. Attendi 60 secondi prima di continuare.")
        # Fa dormire il programma per 60 secondi
        time.sleep(60)
        # Se è passato più di un minuto, resetta il conteggio delle richieste e il tempo di inizio
        mainTool.start_time = time.time()
        mainTool.requests_count = 0


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




