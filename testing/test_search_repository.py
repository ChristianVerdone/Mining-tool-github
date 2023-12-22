"""
Test unitari relativi al file search_repository.py
"""
from io import StringIO
from unittest.mock import patch
from mock import Mock
import requests

from search_repository import request_github, controller_repo


# Test per:
# 1) testare la funzione request_github
# 2) Simulare la risposta della richesta API
def test_controller_repo_2(monkeypatch):
    # Inserisci il tuo token
    token = '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'

    # Input simulati
    inputs = iter([
        r'D:\UNIVERSITA\INGEGNERIA_DEL_SOFTWARE\Mining-tool-github',  # Path della repo dove si cerca il file
        'repositories',
        'esci'
    ])

    # Funzione di input simulato
    def mock_input(_):
        return next(inputs)

    # Simulazione della funzione input
    monkeypatch.setattr('builtins.input', mock_input)

    # Test della funzione controller_repo
    with patch('search_repository.request_github') as mock_request:
        # Mock per simulare la risposta della richiesta API
        mock_request.side_effect = [
            Mock(status_code=200),  # Simulazione di una richiesta con successo
            Mock(status_code=404)  # Simulazione di una richiesta con codice di stato 404
        ]

        # Chiamata alla funzione da testare
        controller_repo(token)

    # Verifica che la funzione request_github sia stata chiamata per ogni linea
    mock_request.assert_any_call(token, "tensorflow", "tensorflow")
    mock_request.assert_any_call(token, "scikit-learn", "scikit-learn")


# Test con percorso del file esistente
# Ogni riga del file è del tipo owner\repository
def test_controller_repo(monkeypatch):
    # Inserisci il tuo token
    token = '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'

    inputs = iter([
        r'D:\UNIVERSITA\INGEGNERIA_DEL_SOFTWARE\Mining-tool-github',  # Path della repo dove si cerca il file
        'repositories',
        'esci'
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('builtins.open', create=True) as mock_open, \
            patch('request_error_handler.request_error_handler') as mock_err:
        controller_repo(token)

    mock_open.assert_called()
    # Verifica che la funzione request_error_handler non sia stata chiamata
    mock_err.assert_not_called()


# Test con file che non esiste
def test_controller_repo_not_file(monkeypatch, capsys):
    # Inserisci il tuo token
    token = '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'
    inputs = iter([
        r'D:\UNIVERSITA\INGEGNERIA_DEL_SOFTWARE\Mining-tool-github',  # Path della repo dove si cerca il file
        'file_not_exists'
    ])
    path_file = r'D:\UNIVERSITA\INGEGNERIA_DEL_SOFTWARE\Mining-tool-github/file_not_exists.txt'

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('builtins.open', create=True) as mock_open:
        controller_repo(token)

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert f"Il percorso '{path_file}' non esiste." in captured.out
    mock_open.assert_not_called()


# Test con percorso che non esiste
def test_controller_repo_not_path(monkeypatch, capsys):
    # Inserisci il tuo token
    token = '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'
    path = 'C:path_not_exist'

    monkeypatch.setattr('builtins.input', lambda _: path)

    with patch('builtins.open', create=True) as mock_open:
        controller_repo(token)

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert f"Il percorso '{path}' non esiste " in captured.out
    mock_open.assert_not_called()


# Test con input = esci
def test_controller_repo_esc(monkeypatch, capsys):
    # Inserisci il tuo token
    token = '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'
    path = 'esci'

    monkeypatch.setattr('builtins.input', lambda _: path)

    with patch('builtins.open', create=True) as mock_open, \
            patch('os.path.exists') as mock_os_path:
        controller_repo(token)

    # Asserzioni
    mock_os_path.assert_not_called()
    mock_open.assert_not_called()


# Test: verifica è possibile effettuare la richiesta
# passano come parametri: token, owner, repository
def test_request_github():
    # Parametri di esempio
    token = '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'  # Sostituire il token con il proprio e ricordarsi di rimuoverlo
    owner = 'tensorflow'
    repository = 'tensorflow'

    # Mock della risposta della richiesta GET
    class MockResponse(requests.Response):
        def __init__(self, status_code, headers):
            super().__init__()
            self.status_code = status_code
            self.headers = headers

    # Simuliamo una risposta con un codice di stato 200 OK e headers di rate limit
    headers = {'X-RateLimit-Remaining': '500',
               'X-RateLimit-Reset': '1609459200'}  # Esempio di headers per il rate limit

    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse(200, headers)

        # Eseguiamo la funzione
        response = request_github(token, owner, repository)

    # Assicuriamoci che la richiesta GET sia stata effettuata con i parametri corretti
    mock_get.assert_called_with(f'https://api.github.com/repos/{owner}/{repository}',
                                headers={'Authorization': 'Bearer ' + token},
                                timeout=30)

    # Assicuriamoci che la funzione abbia restituito una risposta
    assert isinstance(response, requests.Response)
    assert response.status_code == 200
    assert response.headers['X-RateLimit-Remaining'] == '500'
    assert response.headers['X-RateLimit-Reset'] == '1609459200'
