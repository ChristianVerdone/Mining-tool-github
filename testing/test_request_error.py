import request_error_handler


def test_request_error_not_modified(capsys):
    request_error_handler.request_error_handler(304)

    captured = capsys.readouterr()

    # Verifica che l'output includa 'NOT MODIFIED: Non ci sono nuovi dati da restituire.'
    assert 'NOT MODIFIED: Non ci sono nuovi dati da restituire.' in captured.out


def test_request_error_FORBIDDEN(capsys):
    request_error_handler.request_error_handler(403)

    captured = capsys.readouterr()

    # Verifica che l'output includa 'FORBIDDEN: La richiesta è stata rifiutata. Consultare il messaggio allegato per il
    # motivo specifico (molto probabilmente per aver superato il limite di richieste).'
    s = ('FORBIDDEN: La richiesta è stata rifiutata. Consultare il messaggio allegato per il motivo specifico '
         '(molto probabilmente per aver superato il limite di richieste).')
    assert s in captured.out


def test_request_error_NOT_ACCEPTABLE(capsys):
    request_error_handler.request_error_handler(406)

    captured = capsys.readouterr()

    # Verifica che l'output includa 'NOT ACCEPTABLE: La richiesta ha specificato un formato non valido.'
    s = 'Errore nella richiesta: 406\nNOT ACCEPTABLE: La richiesta ha specificato un formato non valido.\n'
    assert s in captured


def test_request_error_INTERNAL_SERVER_ERROR(capsys):
    request_error_handler.request_error_handler(500)

    captured = capsys.readouterr()

    # Verifica che l'output includa 'INTERNAL_SERVER_ERROR: Qualcosa è andato storto.'
    s = 'Errore nella richiesta: 500\nINTERNAL SERVER ERROR: Qualcosa è andato storto.\n'
    assert s in captured.out


def test_request_error_BAD_GATEWAY(capsys):
    request_error_handler.request_error_handler(502)

    captured = capsys.readouterr()
    # Verifica che l'output includa 'Errore nella richiesta: 502\nBAD GATEWAY: Il servizio non è disponibile oppure è
    # in fase di aggiornamento. Riprova più tardi.\n'
    s = ('Errore nella richiesta: 502\nBAD GATEWAY: Il servizio non è disponibile oppure è in fase di aggiornamento.'
         ' Riprova più tardi.\n')
    assert s in captured.out


def test_request_error_SERVICE_UNAVAILABLE(capsys):
    request_error_handler.request_error_handler(503)

    captured = capsys.readouterr()
    # Verifica che l'output includa 'Errore nella richiesta: 503\nSERVICE UNAVAILABLE: Il servizio è attivo,
    # ma sovraccarico di richieste. Riprova più tardi.\n'
    s = ('Errore nella richiesta: 503\nSERVICE UNAVAILABLE: Il servizio è attivo, ma sovraccarico di richieste. '
         'Riprova più tardi.\n')
    assert s in captured.out


def test_request_error_GATEWAY_TIMEOUT(capsys):
    request_error_handler.request_error_handler(504)

    captured = capsys.readouterr()
    # Verifica che l'output includa 'Errore nella richiesta: 504\nGATEWAY TIMEOUT: I server sono attivi,
    # ma la richiesta non può essere servita a causa di un fallimento all'interno del nostro stack. Riprova più tardi.\n'
    s = ("Errore nella richiesta: 504\nGATEWAY TIMEOUT: I server sono attivi, ma la richiesta non può essere servita a"
         " causa di un fallimento all'interno del nostro stack. Riprova più tardi.\n")
    assert s in captured.out


def test_request_error_token_assente(capsys):
    request_error_handler.request_error_handler(505)

    captured = capsys.readouterr()
    # Verifica che l'output includa 'Errore nella richiesta: 505\ntoken assente, impossibile eseguire correttamente
    # le operazioni di mining, inserire un token valido.\n'
    s = ("Errore nella richiesta: 505\ntoken assente, impossibile eseguire correttamente le operazioni di mining, "
         "inserire un token valido.\n")
    assert s in captured.out


def test_request_error_generic(capsys):
    request_error_handler.request_error_handler(0)

    captured = capsys.readouterr()
    # Verifica che l'output includa 'Errore generico nella richiesta'
    s = 'Errore generico nella richiesta'
    assert s in captured.out


def test_request_error_NOT_FOUND(capsys):
    request_error_handler.request_error_handler(404)

    captured = capsys.readouterr()
    # Verifica che l'output includa 'Errore nella richiesta: NOT FOUND: L'URI richiesto non è valido o la risorsa richiesta non esiste.
    s = ("Errore nella richiesta: 404\nNOT FOUND: L'URI richiesto non è valido o la risorsa richiesta non esiste.")
    assert s in captured.out