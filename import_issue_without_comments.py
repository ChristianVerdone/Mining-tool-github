import os
import json
from datetime import datetime
import requests
import rate_limit
import mainTool
import rate_limit_handler
import request_error_handler


def request_github_issues(token, owner, repository, i):
    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues?per_page=100&page={i}'

    tok = f'{token}'
    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer ' + tok}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers, timeout=30)

    mainTool.requests_count += 1
    rate_limit.rate_minute()
    rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                 response.headers['X-RateLimit-Reset'])

    print(f'richiesta {i}')
    return response


def save_github_issues_without_comments(token, owner, repository):
    # Richiedi all'utente di inserire l'owner e il repository
    if owner is None:
        owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    if repository is None:
        repository = input("Inserisci il nome del repository su GitHub: ")
    if token is None:
        request_error_handler.request_error_handler(505)
        return

    # Aggiungi un timestamp alle informazioni delle issue
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    issues_folder = make_issues_directory(repository)

    # Costruisci il percorso del file JSON con il timestamp nel titolo
    file_path = os.path.join(issues_folder, f'issues_without_comments_{timestamp}.json')
    i = 1
    temp = None
    while True:
        response = request_github_issues(token, owner, repository, i)
        i = i + 1
        if response.status_code == 200:
            # La risposta è avvenuta con successo
            issues = response.json()
            # Se l'oggetto json issues è vuoto allora esco dal ciclo perchè ho raggiunto la fine degli elementi da collezionare
            if not issues:
                break

            if temp is None:
                temp = issues
            # altrimenti inserisco in coda a temp gli elementi delle issues successive
            else:
                temp.extend(issues)
        else:
            request_error_handler.request_error_handler(response.status_code)
            return

    # Salva le informazioni delle issue e dei commenti in un file JSON
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(temp, json_file, ensure_ascii=False, indent=4)
    print(f"Le informazioni delle issue sono state salvate con successo nel file '{file_path}'")


def make_issues_directory(repository):
    # Creare la cartella principale con il nome del repository
    repository_folder = f'{repository}_data'
    if not os.path.exists(repository_folder):
        os.makedirs(repository_folder)

    # Creare la sottocartella con il nome "issues"
    issues_folder = os.path.join(repository_folder, 'issues')
    if not os.path.exists(issues_folder):
        os.makedirs(issues_folder)

    return issues_folder
