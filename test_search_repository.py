import requests
from unittest.mock import patch, Mock
from search_repository import request_github, controller_repo 
import pytest 

# Test con percorso del file esistente
# Ogni riga del file è del tipo owner\repository         
def test_controller_repo(monkeypatch):
    # Insierisci il tuo token
    token = 'Your_token'

    inputs = iter([
        'C:\\Users\\angel\\Desktop',
        'repositories',
        'esci'
    ])
    
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('builtins.open', create=True) as mock_open:
        controller_repo(token)

    mock_open.assert_called()


# Test: verifica è possibile effettuare la richiesta
# passanfo come parametri: token, owner, repository 
def test_request_github():
    # Parametri di esempio
    token = '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' # Sostituire il token con il proprio e ricordarsi di rimuoverlo
    owner = 'tensorflow'
    repository = 'tensorflow'

    # Mock della risposta della richiesta GET
    class MockResponse(requests.Response):
        def __init__(self, status_code, headers):
            super().__init__()
            self.status_code = status_code
            self.headers = headers

    # Simuliamo una risposta con un codice di stato 200 OK e headers di rate limit
    headers = {'X-RateLimit-Remaining': '500', 'X-RateLimit-Reset': '1609459200'}  # Esempio di headers per il rate limit
    
    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse(200, headers)
        
        # Eseguiamo la funzione
        response = request_github(token, owner, repository)

    # Assicuriamoci che la richiesta GET sia stata effettuata con i parametri corretti
    mock_get.assert_called_with(f'https://api.github.com/repos/{owner}/{repository}', headers={'Authorization': 'Bearer ' + token})
    
    # Assicuriamoci che la funzione abbia restituito una risposta
    assert isinstance(response, requests.Response)
    assert response.status_code == 200
    assert response.headers['X-RateLimit-Remaining'] == '500'
    assert response.headers['X-RateLimit-Reset'] == '1609459200'
