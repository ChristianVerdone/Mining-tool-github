def request_error_handler(status_code):
    if status_code == 304:
        print(f"Errore nella richiesta: {status_code}")
        print("NOT MODIFIED: Non ci sono nuovi dati da restituire.")

    elif status_code == 401:
        print(f"Errore nella richiesta: {status_code}")
        print("UNAUTHORIZED: Le credenziali di autenticazione mancano, o se fornite non sono valide o "
              "non sono sufficienti per accedere alla risorsa.")

    elif status_code == 403:
        print(f"Errore nella richiesta: {status_code}")
        print("FORBIDDEN: La richiesta è stata rifiutata. Consultare il messaggio allegato per il motivo specifico "
              "(molto probabilmente per aver superato il limite di richieste).")

    elif status_code == 404:
        print(f"Errore nella richiesta: {status_code}")
        print("NOT FOUND: L'URI richiesto non è valido o la risorsa richiesta non esiste.")

    elif status_code == 406:
        print(f"Errore nella richiesta: {status_code}")
        print("NOT ACCEPTABLE: La richiesta ha specificato un formato non valido.")

    elif status_code == 500:
        print(f"Errore nella richiesta: {status_code}")
        print("INTERNAL SERVER ERROR: Qualcosa è andato storto.")

    elif status_code == 502:
        print(f"Errore nella richiesta: {status_code}")
        print("BAD GATEWAY: Il servizio non è disponibile oppure è in fase di aggiornamento. Riprova più tardi.")

    elif status_code == 503:
        print(f"Errore nella richiesta: {status_code}")
        print("SERVICE UNAVAILABLE: Il servizio è attivo, ma sovraccarico di richieste. Riprova più tardi.")

    elif status_code == 504:
        print(f"Errore nella richiesta: {status_code}")
        print("GATEWAY TIMEOUT: I server sono attivi, ma la richiesta non può essere servita a causa di un fallimento "
              "all'interno del nostro stack. Riprova più tardi.")

    elif status_code == 505:
        print(f"Errore nella richiesta: {status_code}")
        print("token assente, impossibile eseguire correttamente le operazioni di mining, inserire un token valido.")

    else:
        print("Errore generico nella richiesta")
