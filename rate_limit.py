# Prima di chiamare il metodo dobbiamo tenere traccia delle richieste e del tempo 
# Provato con l'azione search_repo 
# sostituendo 900 con 3 richieste possibili al minuto e ponendo nel file .txt 8 repository 

import time
import mainTool


# Passiamo il tempo di inizio e il numero di richieste fino a quel momento
def rate_minute():
    start_time = mainTool.start_time
    request_count= mainTool.requests_count

    # tempo corrente
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

    