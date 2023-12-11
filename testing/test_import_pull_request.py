import json
import os
import tempfile
from unittest.mock import patch

import pytest
import requests
import coverage
import import_pull_requests

def test_input_vuoto():
    # Inserisci un input vuoto per l'owner e il repository.
    owner = ""
    repository = ""
    token = ""

    with patch('request_error_handler.request_error_handler') as pyEmpty:
        import_pull_requests.save_github_pull_requests(token, owner, repository)

    pyEmpty.assert_called()

def test_input_non_valido():
    # Inserisci un input non valido per l'owner o il repository.
    owner = "non_esistente"
    repository = "non_esistente"
    token = "non_esistente"

    with patch('request_error_handler.request_error_handler') as pyNotvalid:
        import_pull_requests.save_github_pull_requests(token, owner, repository)

    pyNotvalid.assert_called()

def test_flusso_di_controllo():
    # Prova a eseguire il codice senza un token GitHub valido.
    with patch('request_error_handler.request_error_handler') as NotToken:
         import_pull_requests.save_github_pull_requests(None, "tensorflow", "tensorflow")

    NotToken.assert_called()

def test_output():
    # Verifica che il file JSON sia stato creato, da cambaire il file json, (bisogna prendere uno per le pull request)
    with open('tensorflow_data/issues/issues_with_comments_2023-11-21_20-20-31.json', "r", encoding='utf-8') as json_file:
        pullrequests = json.load(json_file)

    assert len(pullrequests) > 0

    # Verifica che il file JSON contenga le informazioni corrette sui commenti.
    for pullrequest in pullrequests:
        assert isinstance(pullrequest, dict)
        assert "number" in pullrequest
        assert "title" in pullrequest
        assert "state" in pullrequest
        assert "html_url" in pullrequest
        if pullrequest["comments"] > 0:
            for comment in pullrequest["comments_content"]:
                assert isinstance(comment, dict)
                assert "user" in comment
                assert "login" in comment["user"]
                assert "body" in comment

def test_call_rate_limit():

    with patch('rate_limit_handler.wait_for_rate_limit_reset') as pyRateLimit:
        import_pull_requests.save_github_pull_requests('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', "jmpoep",
                                         "vmprotect-3.5.1")

    pyRateLimit.assert_called()

def test_not_pull_request():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        import_pull_requests.save_github_pull_requests('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', 'keras-team',
                                         'keras-core')

        # Verifica che il file JSON sia stato creato.
        assert os.path.exists(tmp_file.name)
        dim = os.path.getsize(tmp_file.name)
        assert dim == 0


# testiamo la situazione in cui riceviamo una risposa con status code != 200 per i commenti di una issue
def test_import_pull_requests_comments_status_error():
    pullrequest = {"number": None}

    with patch('request_error_handler.request_error_handler') as ResponseError:
        response = import_pull_requests.save_github_pull_requests("token", "owner", "repo", pullrequest)

    ResponseError.assert_called()
    assert response == None