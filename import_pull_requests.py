import os
import requests
import json

import rate_limit_handler
import request_error_handler
#import time
from datetime import datetime


def request_github_pull_requests(token, owner, repository, i):
    # Costruisci l'URL dell'API GitHub per ottenere le pull request
    api_url = f'https://api.github.com/repos/{owner}/{repository}/pulls?per_page=100&page={i}'

    # Utilizza il token di Github per autenticarsi 
    headers = {'Authorization': 'Bearer ' + token}

    # GET request al GitHub API
    response = requests.get(api_url, headers=headers)
    print(f'richiesta {i}')
    rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                 response.headers['X-RateLimit-Reset'])

    return response


def save_github_pull_requests(token):
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    pull_requests_folder = make_pull_requests_directory(repository)
    file_path = os.path.join(pull_requests_folder, f'pull_requests_{timestamp}.json')
    i = 1
    temp = None

    while True:
        response = request_github_pull_requests(token, owner, repository, i)

        i = i + 1
        # Continua con il resto del codice per ottenere le pull request
        if response.status_code == 200:
            pull_requests = response.json()
            if not pull_requests:
                break

            for pull_request in pull_requests:
                # print_pull_request(pull_request)

                comments = import_pull_request_comments(token, owner, repository, pull_request)
                if comments is None:
                    pull_request['comments_content'] = comments
                    return

                # print_pull_request_comments(comments)
                pull_request['comments_content'] = comments

            if temp is None:
                temp = pull_requests
            else:
                temp.extend(pull_requests)

        else:
            request_error_handler.request_error_handler(response.status_code)
            return  # Esce dalla funzione

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(temp, json_file, ensure_ascii=False, indent=4)
    print(f"Le informazioni sulle pull request sono state salvate con successo nel file '{file_path}'")


def make_pull_requests_directory(repository):
    # Creare la cartella principale con il nome del repository
    repository_folder = f'{repository}_data'
    if not os.path.exists(repository_folder):
        os.makedirs(repository_folder)

    # Creare la sottocartella con il nome "pull request"
    pull_requests_folder = os.path.join(repository_folder, 'pull_requests')
    if not os.path.exists(pull_requests_folder):
        os.makedirs(pull_requests_folder)

    return pull_requests_folder


def import_pull_request_comments(token, owner, repository, pull_request):
    # Ottieni i commenti delle pull request
    comments_url = f'https://api.github.com/repos/{owner}/{repository}/pulls/{pull_request["number"]}/comments'
    headers = {'Authorization': 'Bearer ' + token}
    comments_response = requests.get(comments_url, headers=headers)
    rate_limit_handler.wait_for_rate_limit_reset(comments_response.headers['X-RateLimit-Remaining'],
                                                 comments_response.headers['X-RateLimit-Reset'])
    if comments_response.status_code != 200:
        request_error_handler.request_error_handler(comments_response.status_code)
        comments = None
        return comments

    comments = comments_response.json()
    return comments


def print_pull_request(pull_request):
    # Stampa le informazioni sulle issue e i relativi commenti sulla console
    print(f"Pull Request #{pull_request['number']}:")
    print(f"  Titolo: {pull_request['title']}")
    print(f"  Stato: {pull_request['state']}")
    print(f"  URL: {pull_request['html_url']}")


def print_pull_request_comments(comments):
    # Stampa i commenti
    print("  Commenti:")
    for comment in comments:
        print(f"    {comment['user']['login']}: {comment['body']}")
    print('\n' + '-' * 50 + '\n')  # Separatore per chiarezza
