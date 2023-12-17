import json
import os
import shutil
from unittest.mock import patch

import pytest

import function_filter


@pytest.fixture(scope="function")
def temp_folder(tmp_path):
    return tmp_path / "test_folder"


# Test con input:
# 1) path
# 2) issues
# 3) esc
def test_filter_github_exit(monkeypatch, capsys):
    user_inputs = iter([
        'path',  # Simula l'input 'path'
        'issues',  # Simula l'input 'issues'
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Uscita dalla funzione." in captured.out


# Test con input:
# 1) path
# 2) pull_request
# 3) esc
def test_filter_github_exit_pr(monkeypatch, capsys):
    user_inputs = iter([
        'path',  # Simula l'input 'path'
        'pull_request',  # Simula l'input 'issues'
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Uscita dalla funzione." in captured.out


# Test con input:
# 1) path
# 2) issues
# 3) C:\Users\angel\Desktop 
# 4) issues_with_comments_2023-11-16_19-05-36
# 5) open
# 6) glemaitre
# 7) esc
def test_filter_github_success(monkeypatch, capsys):
    user_inputs = iter([
        'path',  # Simula l'input 'path'
        'issues',  # Simula l'input 'issues'
        # Si inserisce un percorso che dipende da chi esegue il test dove si vuole cercare il file
        '',  # Simula l'input del percorso
        'issues_with_comments_2023-11-16_10-53-48',
        'open',
        'glemaitre',
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Issue filtrate salvate con successo in:" in captured.out


# Test con input:
# 1) path
# 2) pull_request
# 3) C:\\Users\\angel\\Desktop
# 4) pull_requests_with_comments_2023-11-15_17-24-48
# 5) open
# 6) elfringham
# 7) esc
def test_filter_github_success_pr(monkeypatch, capsys):
    user_inputs = iter([
        'path',  # Simula l'input 'path'
        'pull_request',  # Simula l'input 'issues'
        # Si inserisce un percorso che dipende da chi esegue il test dove si vuole cercare il file
        '',  # Simula l'input del percorso
        # Si utilizza un file presente nella directory
        'pull_requests_2023-11-20_11-02-58',
        'open',
        'elfringham',
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Pull request filtrate salvate con successo in:" in captured.out


# Test con input:
# 1) repository
# 2) issues
# 3) esc
def test_filter_github_repo_exit(monkeypatch, capsys):
    user_inputs = iter([
        'repository',  # Simula l'input 'path'
        'issues',  # Simula l'input 'issues'
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Uscita dalla funzione." in captured.out


# Test con input:
# 1) repository
# 2) issues
# 3) tensorflow (repository specificato dall'utente)
# 4) issues_with_comments_2023-11-22_08-15-59 (nome del file)
# 5) open
# 6) psunn
# 7) esc
def test_filter_github_repo_success(monkeypatch, capsys):
    user_inputs = iter([
        'repository',  # Simula l'input 'path'
        'issues',  # Simula l'input 'issues'
        'tensorflow',  # Simula l'input del percorso
        'issues_with_comments_2023-11-16_10-53-48',
        'open',
        'psunn',
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Issue filtrate salvate con successo in:" in captured.out


# Test con input:
# 1) repository
# 2) pull_request
# 3) esc
def test_filter_github_repo_exit_pr(monkeypatch, capsys):
    user_inputs = iter([
        'repository',  # Simula l'input 'path'
        'pull_request',  # Simula l'input 'issues'
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Uscita dalla funzione." in captured.out


# Test con input:
# 1) repository
# 2) issues
# 3) tensorflow (repository specificato dall'utente)
# 4) pull_requests_with_comments_2023-11-15_17-24-48 (nome del file)
# 5) open
# 6) elfringham
# 7) esc
def test_filter_github_repo_success_pr(monkeypatch, capsys):
    user_inputs = iter([
        'repository',  # Simula l'input 'path'
        'pull_request',  # Simula l'input 'issues'
        'tensorflow',  # Simula l'input del percorso
        'pull_requests_2023-11-20_11-02-58',
        'open',
        'elfringham',
        'esc'  # Simula l'input 'esc' per uscire
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(user_inputs))

    # Esegui la funzione filter_github()
    function_filter.filter_github()

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    # Esegui le asserzioni
    assert "Pull request filtrate salvate con successo in:" in captured.out


# Test: verifica funzione di filtraggio issues passando il path
# per stato e autore
def test_filter_issues_by_path(temp_folder):
    # Dati di esempio per il test
    test_data = [
        {"id": 1, "state": "open", "user": {"login": "user1"}},
        {"id": 2, "state": "closed", "user": {"login": "user2"}},
        {"id": 3, "state": "open", "user": {"login": "user1"}}
    ]

    # Creazione della cartella temporanea se non esiste
    os.makedirs(temp_folder, exist_ok=True)

    # Creazione della cartella temporanea e salvataggio dei dati di test in un file JSON
    test_file_path = temp_folder / "test_issues.json"

    with open(test_file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, indent=4)

    # Chiamata della funzione di filtraggio con filtri specifici
    status_filter = "open"
    author_filter = "user1"
    filtered_i_file_path = function_filter.filter_issues_by_path(test_file_path, status_filter, author_filter)

    # Verifica che il file filtrato sia stato creato correttamente
    assert os.path.exists(filtered_i_file_path)
    assert os.path.isfile(filtered_i_file_path)

    # Verifica se i dati filtrati corrispondono ai criteri specificati
    with open(filtered_i_file_path, 'r', encoding='utf-8') as file:
        filtered_data = json.load(file)
        for pull_request in filtered_data:
            assert pull_request['state'] == "open"
            assert pull_request['user']['login'] == "user1"

    # Elimina la cartella temporanea e tutti i suoi contenuti
    shutil.rmtree(temp_folder)


# Test: verifica funzione di filtraggio pull request passando il path
# per stato e autore
def test_filter_pull_request_by_path(temp_folder):
    # Dati di esempio per il test
    test_data = [
        {"id": 1, "state": "open", "user": {"login": "user1"}},
        {"id": 2, "state": "closed", "user": {"login": "user2"}},
        {"id": 3, "state": "open", "user": {"login": "user1"}}
    ]

    # Creazione della cartella temporanea se non esiste
    os.makedirs(temp_folder, exist_ok=True)

    # Creazione della cartella temporanea e salvataggio dei dati di test in un file JSON
    test_file_path = temp_folder / "test_pull_requests.json"

    with open(test_file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, indent=4)

    # Chiamata della funzione di filtraggio con filtri specifici
    status_filter = "open"
    author_filter = "user1"
    filtered_pr_file_path = function_filter.filter_pull_request_by_path(test_file_path, status_filter, author_filter)

    # Verifica che il file filtrato sia stato creato correttamente
    assert os.path.exists(filtered_pr_file_path)
    assert os.path.isfile(filtered_pr_file_path)

    # Verifica se i dati filtrati corrispondono ai criteri specificati
    with open(filtered_pr_file_path, 'r', encoding='utf-8') as file:
        filtered_data = json.load(file)
        for pull_request in filtered_data:
            assert pull_request['state'] == "open"
            assert pull_request['user']['login'] == "user1"

    # Elimina la cartella temporanea e tutti i suoi contenuti
    shutil.rmtree(temp_folder)


# Test: verifica funzione di filtraggio issues
# per stato e autore
def test_filter_github_issues(temp_folder):
    # Dati di esempio per il test
    repository = "example_repo"
    test_data = [
        {"id": 1, "state": "open", "user": {"login": "user1"}},
        {"id": 2, "state": "closed", "user": {"login": "user2"}},
        {"id": 3, "state": "open", "user": {"login": "user1"}}
    ]

    # Creazione della cartella temporanea se non esiste
    os.makedirs(temp_folder, exist_ok=True)

    test_file_path = temp_folder / "test_issues.json"

    # Salvataggio dei dati di test in un file JSON temporaneo
    with open(test_file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, indent=4)

    # Chiamata della funzione di filtraggio con i filtri specifici
    status_filter = "open"
    author_filter = "user1"
    filtered_i_file_path = function_filter.filter_github_issues(repository, test_file_path, status_filter,
                                                                author_filter)

    # Verifica che il file filtrato sia stato creato correttamente nel percorso restituito dalla funzione
    assert os.path.exists(filtered_i_file_path)
    assert os.path.isfile(filtered_i_file_path)

    # Verifica se i dati filtrati corrispondono ai criteri specificati
    with open(filtered_i_file_path, 'r', encoding='utf-8') as file:
        filtered_data = json.load(file)
        for pull_request in filtered_data:
            assert pull_request['state'] == "open"
            assert pull_request['user']['login'] == "user1"

    # Elimina la cartella temporanea e tutti i suoi contenuti
    shutil.rmtree(temp_folder)


# Test: verifica funzione di filtraggio pull request
# per stato e autore
def test_filter_github_pull_request(temp_folder):
    # Dati di esempio per il test
    repository = "example_repo"
    test_data = [
        {"id": 1, "state": "open", "user": {"login": "user1"}},
        {"id": 2, "state": "closed", "user": {"login": "user2"}},
        {"id": 3, "state": "open", "user": {"login": "user1"}}
    ]

    # Creazione della cartella temporanea se non esiste
    os.makedirs(temp_folder, exist_ok=True)

    test_file_path = temp_folder / "test_pull_requests.json"

    # Salvataggio dei dati di test in un file JSON temporaneo
    with open(test_file_path, 'w', encoding='utf-8') as file:
        json.dump(test_data, file, indent=4)

    # Chiamata della funzione di filtraggio con i filtri specifici
    status_filter = "open"
    author_filter = "user1"
    filtered_pr_file_path = function_filter.filter_github_pull_request(repository, test_file_path, status_filter,
                                                                       author_filter)

    # Verifica che il file filtrato sia stato creato correttamente nel percorso restituito dalla funzione
    assert os.path.exists(filtered_pr_file_path)
    assert os.path.isfile(filtered_pr_file_path)

    # Verifica se i dati filtrati corrispondono ai criteri specificati
    with open(filtered_pr_file_path, 'r', encoding='utf-8') as file:
        filtered_data = json.load(file)
        for pull_request in filtered_data:
            assert pull_request['state'] == "open"
            assert pull_request['user']['login'] == "user1"

    # Elimina la cartella temporanea e tutti i suoi contenuti
    shutil.rmtree(temp_folder)


# Test per verificare la creazione della cartella 
# e il contenuto del file creato
def test_create_folder_creates_directory_and_file(temp_folder):
    filter_data = {"Prova": "value"}  # Dati di esempio per il file JSON
    filter_path = function_filter.create_folder(temp_folder, filter_data)

    # Verifica che la cartella sia stata creata correttamente
    assert os.path.exists(temp_folder)
    assert os.path.isdir(temp_folder)

    # Verifica che il file JSON sia stato creato correttamente nel percorso specificato
    assert os.path.exists(filter_path)
    assert os.path.isfile(filter_path)

    # Verifica che il nome del file contenga 'filter_issues_' e termini con '.json'
    assert filter_path.startswith(str(temp_folder))
    assert filter_path.endswith('.json')
    assert 'filter_issues_' in filter_path

    # Verifica che il file JSON contenga i dati corretti
    with open(filter_path, 'r') as file:
        data = json.load(file)
        assert data == filter_data


# Test con path e file esistente
def test_f_path():
    # Path della directory dove cercare il file
    file_path = r""
    # Path completo della directory con il file alla fine
    path_file = r""

    with patch('os.path.exists') as mock_os_path, \
            patch('builtins.print') as mock_print, \
            patch('builtins.input', return_value="issues_with_comments_2023-11-16_10-53-48"):
        # Il nome del file deve essere uguale a quello che cerchiamo
        result = function_filter.f_path(file_path)

    # print(result)
    mock_os_path.assert_called()
    mock_print.assert_not_called()
    assert result == path_file


# Rivedere -> Test con path e file non esistenti
def test_f_path_non_existing(monkeypatch, capsys):
    path = "C:\\some\\path2"
    path_file = "C:\\some\\path2\\file.json"

    monkeypatch.setattr('builtins.input', lambda _: "file")

    with patch('os.path.exists') as mock_os_path:
        result = function_filter.f_path(path)

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    print(captured.out)
    # print(result)

    mock_os_path.assert_called()
    # Esegui le asserzioni
    # assert f"Il percorso '{path}' non esiste" in captured.out
    # assert f"Il percorso '{result}' non esiste." in captured.out    
    assert result == path_file


# Test con stato presente
def test_state_with_input():
    status_filter = "open"

    with patch("builtins.input", return_value=status_filter) as mock_input, \
            patch('builtins.print') as mock_print:
        result = function_filter.state()

    mock_input.assert_called()
    mock_print.assert_not_called()
    assert result is not None


# Test con stato non presente
def test_state():
    status_filter = ""

    with patch("builtins.input", return_value=status_filter) as mock_input, \
            patch('builtins.print') as mock_print:
        result = function_filter.state()

    mock_input.assert_called()
    mock_print.assert_called_once_with("Lo stato non è presente")
    assert result is None


# Test con utente presente
def test_user_login():
    author_filter = "Angelo"

    with patch('builtins.input', return_value=author_filter) as mock_input, \
            patch('builtins.print') as mock_print:
        result = function_filter.user_login()

    mock_input.assert_called()
    mock_print.assert_not_called()
    assert result == author_filter


# Test che simula l'input vuoto
def test_user_login_empty_input():
    # simula il comportamento della funzione input()
    with patch('builtins.input', return_value=""), \
            patch('builtins.print') as mock_print:
        result = function_filter.user_login()

    mock_print.assert_called_once_with("L'utente non è presente")
    # Verifichiamo che la funzione restituisca None quando l'utente non fornisce alcun input
    assert result is None


def test_user_login_with_input():
    # Definiamo un valore di input simulato
    simulated_input = "Angelo"

    # Simuliamo l'input dell'utente
    with patch('builtins.input', return_value=simulated_input):
        result = function_filter.user_login()

    # Verifichiamo che la funzione restituisca il valore inserito dall'utente
    assert result == simulated_input
