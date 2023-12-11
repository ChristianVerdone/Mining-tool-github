import datetime
import time


def wait_for_rate_limit_reset(remaining, resetTime):
    print(f"resetTime: {resetTime}")
    # Il numero di richieste rimanenti per lo slot time attuale
    temp = int(remaining)
    print(f"Passo 1 -> remaining requests : {remaining}")

    if temp == 0:
        # Questo valore rappresenta il tempo in cui il limite verrà resettato, consentendo nuovamente le richieste.
        # resetTime = rateData['resources']['core']['reset']
        # Ottiene l'istante attuale.
        ms = datetime.datetime.now()

        # Ottiene il timestamp Unix corrente.
        nowTs = int(time.mktime(ms.timetuple()))

        # Calcola la differenza tra il tempo di reset del limite di richieste e il tempo corrente.
        diffTime = int(resetTime) - nowTs
        print(f"Differenza: {diffTime}")

        # Verifica se diffTime è maggiore di zero, cioè se il tempo rimanente prima del reset del limite è positivo.
        if diffTime > 0:
            # Stampa un messaggio che avverte che il limite di richieste API è stato superato e indica il tempo rimanente prima del reset.
            print(f"Superato il limite di richieste API. Attendi {diffTime} secondi prima di continuare.")
            # Fa dormire il programma per diffTime secondi, quindi attende fino a quando
            # il limite di richieste API è stato resettato prima di continuare con le richieste successive.
            time.sleep(diffTime)
            print("Passo 2")
        
        print("Passo 3")
    print("Passo 4")
