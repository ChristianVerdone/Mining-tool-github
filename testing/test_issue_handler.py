import os
from unittest.mock import patch, MagicMock
from datetime import datetime
import json
import pytest

# Importa il modulo contenente le funzioni da testare
import issue_handler  # Assicurati di sostituire "nome_del_tuo_modulo" con il nome effettivo del tuo modulo


@pytest.fixture
def mock_datetime_now():
    with patch('datetime.datetime.now') as mock_now:
        yield mock_now


@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_input():
    with patch('builtins.input') as mock_input:
        yield mock_input


@pytest.fixture
def mock_os_path_exists():
    with patch('os.path.exists') as mock_exists:
        yield mock_exists


@pytest.fixture
def mock_os_makedirs():
    with patch('os.makedirs') as mock_makedirs:
        yield mock_makedirs


@pytest.fixture
def mock_os_join():
    with patch('os.path.join') as mock_join:
        yield mock_join


@pytest.mark.parametrize("response_status_code, expected_call_count", [(200, 1), (404, 1)])
def test_save_github_issues(
        mock_requests_get, mock_input, mock_os_path_exists, mock_os_makedirs, mock_os_join,
        response_status_code, expected_call_count, mock_datetime_now
):
    # Simula una risposta dal server GitHub
    mock_response = MagicMock()
    mock_response.status_code = response_status_code
    mock_response.json.return_value = [{'number': 62390, 'title': 'TFLite GPU: Remove all 16-component vectors',
                                        'state': 'open', 'comments': 0}]
    mock_requests_get.return_value = mock_response

    # Simula la risposta del server GitHub per il conteggio dei commenti
    mock_comments_response = MagicMock()
    mock_comments_response.status_code = 200
    mock_comments_response.json.return_value = [{'user': {'login': 'user1'}, 'body': 'Commento 1'}]

    # Configura il comportamento del mock per la richiesta di commenti
    mock_requests_get.side_effect = [mock_response, mock_comments_response, mock_response]

    # Simula il reset del limite di richieste
    mock_reset_time = '123456789'
    mock_response.headers = {'X-RateLimit-Remaining': '4999', 'X-RateLimit-Reset': mock_reset_time}

    # Simula l'input dell'utente
    mock_input.return_value = 'tensorflow', 'tensorflow'

    # Simula la creazione della directory
    mock_os_path_exists.return_value = False

    # Simula il timestamp corrente
    mock_datetime_now.return_value.strftime.return_value = '2023-12-01_12-00-00'

    # Esegui la funzione da testare
    issue_handler.save_github_issues('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')

    # Verifica che le funzioni siano state chiamate correttamente
    assert mock_os_path_exists.call_count == 1
    assert mock_os_makedirs.call_count == 1
    assert mock_json_dump.call_count == expected_call_count
    assert mock_requests_get.call_count == 3
    assert mock_input.call_count == 2
    assert mock_os_join.call_count == 2


# Aggiungi altri test se necessario

if __name__ == '__main__':
    pytest.main()
