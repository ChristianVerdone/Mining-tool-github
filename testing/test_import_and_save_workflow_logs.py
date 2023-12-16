import json
import os
import tempfile
from unittest.mock import patch

import import_and_save_workflow_logs


def test_make_issue_directory_path_not_exists():
    with patch('os.makedirs') as pyMakeDir:
        import_and_save_workflow_logs.save_github_workflow_logs("token", "test", "test")

    pyMakeDir.assert_called()


def test_input_vuoto():
    # Inserisci un input vuoto per l'owner e il repository.
    owner = ""
    repository = ""
    token = ""

    with patch('request_error_handler.request_error_handler') as pyEmpty:
        import_and_save_workflow_logs.save_github_workflow_logs(token, owner, repository)

    pyEmpty.assert_called()


def test_input_non_valido():
    # Inserisci un input non valido per l'owner o il repository.
    owner = "non_esistente"
    repository = "non_esistente"
    token = "non_esistente"

    with patch('request_error_handler.request_error_handler') as pyNotvalid:
        import_and_save_workflow_logs.save_github_workflow_logs(token, owner, repository)

    pyNotvalid.assert_called()


def test_flusso_di_controllo():
    # Prova a eseguire il codice senza un token GitHub non valido.
    with patch('request_error_handler.request_error_handler') as NotToken:
        import_and_save_workflow_logs.save_github_workflow_logs(None, "tensorflow", "tensorflow")

    NotToken.assert_called()


def test_output():
    # Verifica che il file JSON sia stato creato. #da modificare il file .json
    with open('anything-llm_data/workflow_logs/workflow_logs_2023-12-15_10-44-13.json', "r",
              # da modificare con path giusto
              encoding='utf-8') as json_file:
        workflow_runs = json.load(json_file)

    assert len(workflow_runs) > 0


def test_call_rate_limit():
    with patch('rate_limit_handler.wait_for_rate_limit_reset') as pyRateLimit:
        import_and_save_workflow_logs.save_github_workflow_logs('', "jmpoep",
                                                                "vmprotect-3.5.1")

    pyRateLimit.assert_called()


def test_not_workflow_log():  # metodo da rivedere
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        import_and_save_workflow_logs.save_github_workflow_logs('',
                                                                'geeks-r-us',
                                                                'mqtt-panel')

        # Verifica che il file JSON sia stato creato.
        assert os.path.exists(tmp_file.name)
        dim = os.path.getsize(tmp_file.name)
        assert dim == 0


def test_request_github_workflow_logs():  # da inserire il proprio token prima di eseguire
    i = 0
    response = import_and_save_workflow_logs.get_github_workflow_logs('', 'keras-team',
                                                                      'keras-core', i)
    assert response.status_code == 200
