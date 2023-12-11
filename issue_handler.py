import os
import requests
import json
import rate_limit
import mainTool

import rate_limit_handler
import request_error_handler
from datetime import datetime


def request_github_issues(token, owner, repository, i):
    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues?per_page=100&page={i}'

    tok = f'{token}'
    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer ' + tok}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    mainTool.requests_count += 1
    rate_limit.rate_minute()
    rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                 response.headers['X-RateLimit-Reset'])

    return response


def save_github_issues(token, owner, repository):
    # Richiedi all'utente di inserire l'owner e il repository
    if owner is None:
        owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    if repository is None:
        repository = input("Inserisci il nome del repository su GitHub: ")
    if token is None:
        request_error_handler.request_error_handler(505)

    # Aggiungi un timestamp alle informazioni delle issue
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    issues_folder = make_issues_directory(repository)

    # Costruisci il percorso del file JSON con il timestamp nel titolo
    file_path = os.path.join(issues_folder, f'issues_with_comments_{timestamp}.json')
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

            for issue in issues:
                # Se la issue ha almeno 1 commento allora mi preoccupo di effettuare una richiesta all'API altrimenti me la risparmio
                if issue['comments'] > 0:
                    comments = import_issue_comments(token, owner, repository, issue)
                    # check comments requests
                    if comments is None:
                        return
                else:
                    comments = 0
                # il nuovo campo 'comments_content' viene sempre creato per mantenere coerenti gli elementi del file json
                issue['comments_content'] = comments
            # alla prima iterazione temp sarà None e lo rendo un oggetto json assegnando il valore di issues
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


def import_issue_comments(token, owner, repository, issue):
    # Ottieni i commenti della issue
    comments_url = f'https://api.github.com/repos/{owner}/{repository}/issues/{issue["number"]}/comments'
    headers = {'Authorization': 'Bearer ' + token}
    comments_response = requests.get(comments_url, headers=headers)
    
    mainTool.requests_count += 1
    rate_limit.rate_minute()
    
    rate_limit_handler.wait_for_rate_limit_reset(comments_response.headers['X-RateLimit-Remaining'],
                                                 comments_response.headers['X-RateLimit-Reset'])

    if comments_response.status_code != 200:
        request_error_handler.request_error_handler(comments_response.status_code)
        comments = None
        return comments

    comments = comments_response.json()
    return comments


def print_issue(issue):
    # Stampa le informazioni sulle issue e i relativi commenti sulla console
    print(f"Issue #{issue['number']}:")
    print(f"  Titolo: {issue['title']}")
    print(f"  Stato: {issue['state']}")
    print(f"  URL: {issue['html_url']}")


def print_issue_comments(comments):
    # Stampa i commenti
    print("  Commenti:")
    for comment in comments:
        print(f"    {comment['user']['login']}: {comment['body']}")

    print('\n' + '-' * 30 + '\n')  # Separatore per chiarezza
