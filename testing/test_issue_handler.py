import json
import os
import tempfile
from unittest.mock import patch

import issue_handler


# da modificare per unit testing
def test_make_issue_directory_path_not_exists():
    with patch('os.makedirs') as pyMakeDir:
        issue_handler.save_github_issues("token", "test", "test")

    pyMakeDir.assert_called()


def test_input_vuoto():
    # Inserisci un input vuoto per l'owner e il repository.
    owner = ""
    repository = ""
    token = ""

    with patch('request_error_handler.request_error_handler') as pyEmpty:
        issue_handler.save_github_issues(token, owner, repository)

    pyEmpty.assert_called()


def test_input_non_valido():
    # Inserisci un input non valido per l'owner o il repository.
    owner = "non_esistente"
    repository = "non_esistente"
    token = "non_esistente"

    with patch('request_error_handler.request_error_handler') as pyNotvalid:
        issue_handler.save_github_issues(token, owner, repository)

    pyNotvalid.assert_called()


def test_flusso_di_controllo():
    # Prova a eseguire il codice senza un token GitHub valido.
    with patch('request_error_handler.request_error_handler') as NotToken:
        issue_handler.save_github_issues(None, "tensorflow", "tensorflow")

    NotToken.assert_called()


def test_output():
    # Verifica che il file JSON sia stato creato.
    with open('tensorflow_data/issues/issues_with_comments_2023-11-21_20-20-31.json', "r",
              encoding='utf-8') as json_file:
        issues = json.load(json_file)

    assert len(issues) > 0

    # Verifica che il file JSON contenga le informazioni corrette sui commenti.
    for issue in issues:
        assert isinstance(issue, dict)
        assert "number" in issue
        assert "title" in issue
        assert "state" in issue
        assert "html_url" in issue
        if issue["comments"] > 0:
            for comment in issue["comments_content"]:
                assert isinstance(comment, dict)
                assert "user" in comment
                assert "login" in comment["user"]
                assert "body" in comment


def test_call_rate_limit():
    with patch('rate_limit_handler.wait_for_rate_limit_reset') as pyRateLimit:
        issue_handler.save_github_issues('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', "jmpoep",
                                         "vmprotect-3.5.1")

    pyRateLimit.assert_called()


def test_not_issue():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        issue_handler.save_github_issues('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', 'keras-team',
                                         'keras-core')

        # Verifica che il file JSON sia stato creato.
        assert os.path.exists(tmp_file.name)
        dim = os.path.getsize(tmp_file.name)
        assert dim == 0


def test_request_github_issues():
    i = 0
    response = issue_handler.request_github_issues('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', 'keras-team',
                                                   'keras-core', i)

    assert response.status_code == 200


# da aggiustare n
def test_input_valido():
    with patch('issue_handler.import_issue_comments') as pyHasComments:
        pyHasComments.return_value = {'comment': 'This is a comment'}
        issue_handler.save_github_issues('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', "jmpoep",
                                         "vmprotect-3.5.1")

    pyHasComments.assert_called()


def test_input_valido_no_comments():
    with patch('issue_handler.import_issue_comments') as pyHasComments:
        pyHasComments.return_value = {'comment': 'This is a comment'}
        issue_handler.save_github_issues('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', "ChristianVerdone",
                                         "testing")

    pyHasComments.assert_not_called()


# testiamo la situazione in cui riceviamo una risposa con status code != 200 per i commenti di una issue
def test_import_issue_comments_status_error():
    issue = {"number": None}

    with patch('request_error_handler.request_error_handler') as ResponseError:
        response = issue_handler.import_issue_comments("token", "owner", "repo", issue)

    ResponseError.assert_called()
    assert response is None


def test_import_issue_comments_status_ok():
    issue = {"number": 2}

    with patch('request_error_handler.request_error_handler') as ResponseError:
        response = issue_handler.import_issue_comments("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",
                                                       "jmpoep", "vmprotect-3.5.1", issue)

    ResponseError.assert_not_called()
