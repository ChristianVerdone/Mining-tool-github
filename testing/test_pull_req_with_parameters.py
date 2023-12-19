"""
Test per verificare il file pull_req_with_parameters
"""

from pull_req_with_parameters import request_github_pull_requests, github_pullreq_with_par, \
    make_pull_requests_directory, extract_params_from_pullreq
from unittest.mock import patch


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


# Test per verificare l'uscita dalla funzione
def test_github_pullreq_with_par_exit(capsys, monkeypatch):
    # Inserisci il tuo token
    token = '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'

    inputs = iter([
        'esci',
        'esci'
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    github_pullreq_with_par(token)
    captured = capsys.readouterr()

    assert 'Uscita dalla funzione.' in captured.out


# Test per controllare se la funzione:
# 1) Effettua la richiesta in modo corretto 
# 2) Non viene chiamato alcun errore
# 3) Scrive nel file 
# 4) Infine esce dalla funzione
def test_github_pullreq_with_par(monkeypatch, capsys):
    # Parametri di esempio
    token = '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'  # Sostituire il token con il proprio e ricordarsi di rimuoverlo

    inputs = iter([
        'tensorflow',
        'tensorflow',
        'esci',
        'esci'
    ])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('builtins.open', create=True) as mock_open, \
            patch('request_error_handler.request_error_handler') as mock_err:
        github_pullreq_with_par(token)

    # Cattura l'output stampato durante l'esecuzione della funzione
    captured = capsys.readouterr()

    mock_open.assert_called()
    mock_err.assert_not_called()
    assert 'Uscita dalla funzione.' in captured.out


# Test per verificare la creazione della directory
def test_make_pull_requests_directory():
    repository = "tensorflow"
    repository_folder = "tensorflow_data"

    with patch('os.path.join') as mock_join, \
            patch('os.path.exists') as mock_exists:
        # Chiamata alla funzione
        pull_requests_folder = make_pull_requests_directory(repository)

    mock_join.assert_called_once_with(repository_folder, 'pull_requests')
    mock_exists.assert_called()
    assert pull_requests_folder is not None


# Test per verificare l'estrazione
def test_extract_params_from_pullreq():
    # Esempio di lista di issues
    pull_requests = [
        {
            'url': 'https://api.github.com/repos/octocat/Hello-World/pull_request/1347',
            'number': 1347,
            'title': 'Found a bug',
            'user': {'login': 'user1'},
            'state': 'open',
            'assignee': {'login': 'user2'},
            "node_id": "PR_kwDOArmXAs5gDm9P1",  # Parametro in più per verificare la correttezza
            'comments': 10,  # Parametro in più
            'body': 'Test pull request 1'
        },
        {
            'url': 'https://api.github.com/repos/octocat/Hello-World/pull_request/1348',
            'number': 1348,
            'title': 'Feature request',
            'user': {'login': 'user3'},
            'state': 'closed',
            'assignee': None,
            "node_id": "PR_kwDOArmXAs5gDm9P2",  # Parametro in più per verificare la correttezza
            'comments': 5,  # Parametro in più
            'body': 'Test pull request 2'
        }
    ]

    # Chiamata alla funzione da testare
    params_list = extract_params_from_pullreq(pull_requests)

    # Verifica che la lista dei parametri estratti abbia la lunghezza corretta
    assert len(params_list) == len(pull_requests)

    # Verifica che ciascun elemento della lista dei parametri estratti contenga i campi desiderati
    for extracted_params, pull_request in zip(params_list, pull_requests):
        assert extracted_params['url'] == pull_request['url']
        assert extracted_params['number'] == pull_request['number']
        assert extracted_params['title'] == pull_request['title']
        assert extracted_params['user_login'] == (pull_request['user']['login'] if pull_request['user'] else None)
        assert extracted_params['state'] == pull_request['state']
        assert extracted_params['assignee_login'] == (
            pull_request['assignee']['login'] if pull_request['assignee'] else None)
        assert extracted_params['body'] == pull_request['body']
