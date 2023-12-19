import os
import tempfile
from unittest.mock import patch, MagicMock

import import_pull_requests
from import_pull_requests import request_github_pull_requests


# Test per verificare la richiesta
def test_request_github_pull_requests():
    # Parametri di esempio
    token = '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'  # Sostituire il token con il proprio e ricordarsi di rimuoverlo
    owner = 'tensorflow'
    repository = 'tensorflow'
    i = 1

    with patch('requests.get') as mock_req, \
            patch('rate_limit.rate_minute') as mock_rate, \
            patch('rate_limit_handler.wait_for_rate_limit_reset') as mock_limit:
        # Eseguiamo la funzione
        response = request_github_pull_requests(token, owner, repository, i)

    mock_req.assert_called_once_with(
        f'https://api.github.com/repos/{owner}/{repository}/pulls?per_page=100&page={i}',
        headers={'Authorization': 'Bearer ' + token}
    )
    mock_rate.assert_called()
    mock_limit.assert_called()
    assert response is not None


def test_not_pull_request():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        import_pull_requests.save_github_pull_requests('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', 'keras-team',
                                                       'keras-core')

        # Verifica che il file JSON sia stato creato.
        assert os.path.exists(tmp_file.name)
        dim = os.path.getsize(tmp_file.name)
        assert dim == 0


def test_request_github_pulls():
    i = 0
    response = import_pull_requests.request_github_pull_requests('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',
                                                                 'keras-team', 'keras-core', i)

    assert response.status_code == 200


# da aggiustare n
def test_input_valido():
    with patch('import_pull_requests.import_pull_request_comments') as pyHasComments:
        pyHasComments.return_value = {'comment': 'This is a comment'}
        import_pull_requests.save_github_pull_requests('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', "jmpoep",
                                                       "vmprotect-3.5.1")

    pyHasComments.assert_called()


def test_input_valido_no_comments():
    with patch('import_pull_requests.import_pull_request_comments') as pyHasComments:
        pyHasComments.return_value = {'comment': 'This is a comment'}
        import_pull_requests.save_github_pull_requests('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', "ChristianVerdone",
                                                       "testing")

    pyHasComments.assert_called()


# testiamo la situazione in cui riceviamo una risposa con status code != 200 per i commenti di una issue
def test_import_pull_requests_comments_status_error():
    pullrequest = {"number": None}

    with patch('request_error_handler.request_error_handler') as ResponseError:
        response = import_pull_requests.import_pull_request_comments("token", "owner", "repo",
                                                                     pullrequest)

    ResponseError.assert_called()
    assert response is None


def test_import_pull_requests_no_Token(monkeypatch):
    inputs = iter(['',
                   '',])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    with patch('request_error_handler.request_error_handler') as ResponseError:
        import_pull_requests.save_github_pull_requests(None, None, None)

    ResponseError.assert_called()


def test_import_pull_requests_200():
    with patch('builtins.open', create=True) as mock_open:
        import_pull_requests.save_github_pull_requests('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',
                                                       'tensorflow', 'tensorflow')
    mock_open.assert_called()
