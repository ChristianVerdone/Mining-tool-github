import pytest
from unittest.mock import MagicMock, patch
from import_pull_requests import request_github_pull_requests
import mainTool, rate_limit, rate_limit_handler


@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_main_tool():
    with patch('mainTool') as mock_tool:
        yield mock_tool


@pytest.fixture
def mock_rate_limit():
    with patch('rate_limit') as mock_limit:
        yield mock_limit


@pytest.fixture
def mock_rate_limit_handler():
    with patch('rate_limit_handler') as mock_handler:
        yield mock_handler


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