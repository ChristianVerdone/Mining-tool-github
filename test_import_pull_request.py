import pytest
from unittest.mock import patch, MagicMock, call
import import_pull_requests
import os


def test_request_github_pull_requests():
    token = "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"  #token corretto
    owner = "tensorflow"  #owner corretto 
    repository = "tensorflow" #repo corretto 
    i = 1
    #response_status = 200

    with patch('requests.get') as mock_get, \
            patch('import_pull_requests.rate_limit.rate_minute') as mock_limit, \
            patch('import_pull_requests.rate_limit_handler.wait_for_rate_limit_reset') as mock_limit_handler:
        
        import_pull_requests.request_github_pull_requests(token, owner, repository, i)

        mock_get.assert_called_once_with(
            f'https://api.github.com/repos/{owner}/{repository}/pulls?per_page=100&page={i}',
            headers={'Authorization': 'Bearer ' + token}
        )
        
        # Non va bene
        # response = mock_get.return_value
        # assert response_status == response

        # Verifica che le altre funzioni siano state chiamate
        mock_limit.assert_called_once()
        mock_limit_handler.assert_called_once()

def test_save_github_pull_requests():
    pass

def test_make_pull_requests_directory():
    repository = "test"

    with patch('os.path.exists') as mock_exists, \
         patch('os.makedirs') as mock_makedirs, \
         patch('os.path.join') as mock_os_path:

        # Simula che la directory 'test_data' non esista
        mock_exists.side_effect = [False, False]

        # Chiamata alla funzione da testare
        import_pull_requests.make_pull_requests_directory(repository)

        mock_exists.assert_called()
        mock_makedirs.assert_called()
        
        mock_os_path.assert_called_once_with('test_data', 'pull_requests')

def test_import_pull_request_comments():
    token = "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"  #token corretto
    owner = "tensorflow"  #owner corretto 
    repository = "tensorflow" #repo corretto
    pull_request = {"number": 10}  # Sostituire con una corretta
    
    with patch('requests.get') as mock_get, \
        patch('rate_limit.rate_minute') as mock_rate, \
        patch('rate_limit_handler.wait_for_rate_limit_reset') as mock_rate_handler, \
        patch('request_error_handler.request_error_handler') as mock_error_handler:
        #patch('comments_response.json') as mock_json:
        import_pull_requests.import_pull_request_comments(token, owner, repository, pull_request)

    mock_get.assert_called_once_with(
            f'https://api.github.com/repos/{owner}/{repository}/pulls/{pull_request["number"]}/comments',
            headers={'Authorization': 'Bearer ' + token}
        )

    mock_rate.assert_called()
    mock_rate_handler.assert_called()
    mock_error_handler.assert_called() 
    #mock_error_handler.assert_not_called() 
    #mock_json.assert_called()

def test_import_pull_request_comments_2():
    token = "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"  #token corretto
    owner = "tensorflow"  #owner corretto 
    repository = "tensorflow" #repo corretto
    pull_request = {"number": 10}

    # Simulazione di una risposta di successo
    comments_response = MagicMock()
    comments_response.status_code = 200
    comments_response.json.return_value = {"comment": "Test comment"}
    
    with patch('requests.get') as mock_get, \
        patch('rate_limit.rate_minute') as mock_rate, \
        patch('rate_limit_handler.wait_for_rate_limit_reset') as mock_rate_handler, \
        patch('request_error_handler.request_error_handler') as mock_error_handler:
        
        # Configurazione del comportamento atteso per la richiesta GET
        mock_get.return_value = comments_response
        
        import_pull_requests.import_pull_request_comments(token, owner, repository, pull_request)

    mock_get.assert_called_once_with(
            f'https://api.github.com/repos/{owner}/{repository}/pulls/{pull_request["number"]}/comments',
            headers={'Authorization': 'Bearer ' + token}
        )

    mock_rate.assert_called()
    mock_rate_handler.assert_called()
    
    mock_error_handler.assert_not_called()
    
    # Verifica che il metodo json della risposta sia stato chiamato
    comments_response.json.assert_called_once()

    # Verifica che la funzione restituisca la risposta JSON
    assert import_pull_requests.import_pull_request_comments(token, owner, repository, pull_request) == {"comment": "Test comment"}

def test_print_pull_request():
    pass

def test_print_pull_request_comments():
    pass


#test_request_github_pull_requests()
#test_make_pull_requests_directory()
test_import_pull_request_comments()


















'''
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

    # Verifica che le funzioni correlate siano chiamate correttamente
    mock_main_tool.requests_count += 1
    mock_rate_limit.rate_minute.assert_called_once()
    mock_rate_limit_handler.wait_for_rate_limit_reset.assert_called_once_with(
        '100', '1640398787'
    )

'''