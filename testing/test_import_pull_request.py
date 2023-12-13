import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from import_pull_requests import request_github_pull_requests
import pytest
import requests
import coverage
import import_pull_requests


def test_request_github_pull_request(mock_requests_get, mock_main_tool, mock_rate_limit, mock_rate_limit_handler):
    # Configura il mock per restituire un oggetto Response di successo
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    # Configura il mock per restituire il valore desiderato da X-RateLimit-Remaining e X-RateLimit-Reset
    mock_response.headers = {'X-RateLimit-Remaining': '100', 'X-RateLimit-Reset': '1640398787'}

    # Chiamare la funzione da testare
    result = request_github_pull_requests('fake_token', 'owner', 'repo', 1)

    # Verifica che la chiamata a requests.get sia stata fatta con l'URL corretto
    mock_requests_get.assert_called_once_with(
        'https://api.github.com/repos/owner/repo/pulls?per_page=100&page=1',
        headers={'Authorization': 'Bearer fake_token'}
    )

    # Verifica che la funzione restituisca la response corretta
    assert result == mock_response

    # Verifica che le funzioni correlate siano chiamate correttamente
    mock_main_tool.requests_count += 1
    mock_rate_limit.rate_minute.assert_called_once()
    mock_rate_limit_handler.wait_for_rate_limit_reset.assert_called_once_with(
        '100', '1640398787'
    )


def test_request_github_pull_requests(mock_requests_get, mock_main_tool, mock_rate_limit, mock_rate_limit_handler):
    # Configura il mock per restituire un oggetto Response di successo
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_requests_get.return_value = mock_response

    # Configura il mock per restituire il valore desiderato da X-RateLimit-Remaining e X-RateLimit-Reset
    mock_response.headers = {'X-RateLimit-Remaining': '100', 'X-RateLimit-Reset': '1640398787'}

    # Chiamare la funzione da testare
    result = request_github_pull_requests('fake_token', 'owner', 'repo', 1)

    # Verifica che la chiamata a requests.get sia stata fatta con l'URL corretto
    mock_requests_get.assert_called_once_with(
        'https://api.github.com/repos/owner/repo/pulls?per_page=100&page=1',
        headers={'Authorization': 'Bearer fake_token'}
    )

    # Verifica che la funzione restituisca la response corretta
    assert result == mock_response

    #pyRateLimit.assert_called()


def test_not_pull_request():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        import_pull_requests.save_github_pull_requests('', 'keras-team',
                                                       'keras-core')

        # Verifica che il file JSON sia stato creato.
        assert os.path.exists(tmp_file.name)
        dim = os.path.getsize(tmp_file.name)
        assert dim == 0


def test_request_github_pulls():
    i = 0
    response = import_pull_requests.request_github_pull_requests('',
                                                                 'keras-team', 'keras-core', i)

    assert response.status_code == 200


# da aggiustare n
def test_input_valido():
    with patch('import_pull_requests.import_pull_request_comments') as pyHasComments:
        pyHasComments.return_value = {'comment': 'This is a comment'}
        import_pull_requests.save_github_pull_requests('', "jmpoep",
                                                       "vmprotect-3.5.1")

    pyHasComments.assert_called()


def test_input_valido_no_comments():
    with patch('import_pull_requests.import_pull_request_comments') as pyHasComments:
        pyHasComments.return_value = {'comment': 'This is a comment'}
        import_pull_requests.save_github_pull_requests('', "linexjlin",
                                                       "GPTs")

    pyHasComments.assert_not_called()


# testiamo la situazione in cui riceviamo una risposa con status code != 200 per i commenti di una issue
def test_import_pull_requests_comments_status_error():
    pullrequest = {"number": None}

    with patch('request_error_handler.request_error_handler') as ResponseError:
        response = import_pull_requests.import_pull_request_comments("token", "owner", "repo",
                                                                     pullrequest)

    ResponseError.assert_called()
    assert response == None
