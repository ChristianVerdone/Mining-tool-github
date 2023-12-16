"""
Test per verificare il file issues_with_parameters
"""
from issues_with_parameters import request_github_issues
from unittest.mock import patch
import requests


def test_request_github_issues():
    # Parametri di esempio
    token = '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'
    owner = 'tensorflow'
    repository = 'tensorflow'
    i = 1

    # Mock della risposta della richiesta GET
    class MockResponse(requests.Response):
        def __init__(self, status_code, headers):
            super().__init__()
            self.status_code = status_code
            self.headers = headers

    # Simuliamo una risposta con un codice di stato 200 OK e headers di rate limit
    # Esempio di headers per il rate limit
    headers = {'X-RateLimit-Remaining': '500', 'X-RateLimit-Reset': '1609459200'}

    with patch('requests.get') as mock_get:
        mock_get.return_value = MockResponse(200, headers)

        # Eseguiamo la funzione
        response = request_github_issues(token, owner, repository, i)

    # Assicuriamoci che la richiesta GET sia stata effettuata con i parametri corretti
    mock_get.assert_called_with(
        f'https://api.github.com/repos/{owner}/{repository}/issues?per_page=100&page={i}',
        headers={'Authorization': 'Bearer ' + token})

    # Assicuriamoci che la funzione abbia restituito una risposta
    assert isinstance(response, requests.Response)
    assert response.status_code == 200
    assert response.headers['X-RateLimit-Remaining'] == '500'
    assert response.headers['X-RateLimit-Reset'] == '1609459200'
