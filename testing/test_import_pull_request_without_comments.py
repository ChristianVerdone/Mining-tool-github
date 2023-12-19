import json
import os
import tempfile
from unittest.mock import patch

import import_pull_request_without_comments


# da modificare per unit testing
def test_make_issue_directory_path_not_exists():
    with patch('os.makedirs') as pyMakeDir:
        import_pull_request_without_comments.save_github_pull_requests_without_comments("token", "test",
                                                                                        "test")

    pyMakeDir.assert_called()


def test_input_vuoto():
    # Inserisci un input vuoto per l'owner e il repository.
    owner = ""
    repository = ""
    token = ""

    with patch('request_error_handler.request_error_handler') as pyEmpty:
        import_pull_request_without_comments.save_github_pull_requests_without_comments(token, owner, repository)

    pyEmpty.assert_called()


def test_input_non_valido():
    # Inserisci un input non valido per l'owner o il repository.
    owner = "non_esistente"
    repository = "non_esistente"
    token = "non_esistente"

    with patch('request_error_handler.request_error_handler') as pyNotvalid:
        import_pull_request_without_comments.save_github_pull_requests_without_comments(token, owner, repository)

    pyNotvalid.assert_called()


def test_flusso_di_controllo():
    # Prova a eseguire il codice senza un token GitHub valido.
    with patch('request_error_handler.request_error_handler') as NotToken:
        import_pull_request_without_comments.save_github_pull_requests_without_comments(None, "tensorflow",
                                                                                        "tensorflow")

    NotToken.assert_called()


def test_output():
    # Verifica che il file JSON sia stato creato. #da modificare il file .json
    with open('tensorflow_data/issues/issues_with_comments_2023-11-21_20-20-31.json', "r",
              # da modificare con giusto path
              encoding='utf-8') as json_file:
        pullrequests = json.load(json_file)

    assert len(pullrequests) > 0


def test_call_rate_limit():
    with patch('rate_limit_handler.wait_for_rate_limit_reset') as pyRateLimit:
        import_pull_request_without_comments.save_github_pull_requests_without_comments('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', "jmpoep",
                                                                                        "vmprotect-3.5.1")

    pyRateLimit.assert_called()


def test_not_pull_req_without_comments():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        import_pull_request_without_comments.save_github_pull_requests_without_comments('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', 'keras-team',
                                                                                        'keras-core')

        # Verifica che il file JSON sia stato creato.
        assert os.path.exists(tmp_file.name)
        dim = os.path.getsize(tmp_file.name)
        assert dim == 0


def test_request_github_pull_req_without_comments():
    i = 0
    response = import_pull_request_without_comments.request_github_pull_requests_without_comments('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', 'keras-team',
                                                                                                  'keras-core', i)

    assert response.status_code == 200
