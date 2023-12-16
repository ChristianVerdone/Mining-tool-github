"""
Test unitari relativi al file search_repository.py
"""
from unittest.mock import patch
import requests
from unittest.mock import patch
from search_repository import request_github, controller_repo


# Test con percorso del file esistente
# Ogni riga del file è del tipo owner\repository
def test_controller_repo(monkeypatch):
    # Inserisci il tuo token
    token = ''

    inputs = iter([
        'C:\Users\angel\Desktop\Progetto Ing\Mining-tool-github',
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


# Test con percorso che non esiste
def test_controller_repo_not_path(monkeypatch, capsys):
    # Inserisci il tuo token
    token = ''
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
    token = ''
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
    token = ''  # Sostituire il token con il proprio e ricordarsi di rimuoverlo
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
                                headers={'Authorization': 'Bearer ' + token})

    # Assicuriamoci che la funzione abbia restituito una risposta
    assert isinstance(response, requests.Response)
    assert response.status_code == 200
    assert response.headers['X-RateLimit-Remaining'] == '500'
    assert response.headers['X-RateLimit-Reset'] == '1609459200'
