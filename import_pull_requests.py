import os
import requests
import json

import mainTool
import request_error_handler
import time
from datetime import datetime

def get_rate_limit(token):
    # Costruisci l'URL dell'API GitHub per ottenere le informazioni sul rate limit
    rate_limit_url = 'https://api.github.com/rate_limit'

    # Utilizza il token di GitHub per autenticarsi
    headers = {'Authorization': 'Bearer ' + token}

    # Fai una richiesta GET all'API di GitHub per ottenere le informazioni sul rate limit
    response = requests.get(rate_limit_url, headers=headers)

    if response.status_code == 200:
        rate_limit_info = response.json()
        return rate_limit_info
    else:
        print(f"Errore nell'ottenere le informazioni sul rate limit. Codice di stato: {response.status_code}")
        try:
            error_message = response.json().get('message', 'Nessun messaggio di errore fornito.')
            print(f"Dettagli dell'errore: {error_message}")
        except json.JSONDecodeError:
            print("Errore nella decodifica della risposta JSON.")
        return None
    

def request_github_pull_requests(token, owner, repository, i):

    # Costruisci l'URL dell'API GitHub per ottenere le pull request
    api_url = f'https://api.github.com/repos/{owner}/{repository}/pulls?per_page=100&page={i}'

    # Utilizza il token di Github per autenticarsi 
    headers = {'Authorization': 'Bearer ' + token}

    # GET request al GitHub API
    response = requests.get(api_url, headers=headers)
    print(f'richiesta {i}')
    mainTool.wait_for_rate_limit_reset(headers)

    return response


def save_github_pull_requests(token):
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")
    headers = {'Authorization': 'Bearer ' + token}
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    pull_requests_folder = make_pull_requests_directory(repository)
    file_path = os.path.join(pull_requests_folder, f'pull_requests_{timestamp}.json')
    i = 1
    temp = None

    while True:
        response = request_github_pull_requests(token, owner, repository, i)

        i = i + 1
        # Verifica lo stato corrente del rate limit
        '''rate_limit_info = get_rate_limit(token)
        if rate_limit_info:
            remaining_requests = rate_limit_info['resources']['core']['remaining']
            reset_timestamp = rate_limit_info['resources']['core']['reset']
            reset_time = datetime.fromtimestamp(reset_timestamp)
            print(f"Richieste rimanenti: {remaining_requests}")
            print(f"Limite di frequenza si ripristina il: {reset_time}")
    
            # Se le richieste rimanenti sono basse, potresti considerare di attendere prima di fare ulteriori richieste.
            if remaining_requests < 10:
                wait_time = reset_time - datetime.now()
                print(f"Attesa per {wait_time.seconds} secondi prima di fare ulteriori richieste.")
                time.sleep(wait_time.seconds)
    
            # Continua solo se il rate limit consente ulteriori richieste
            if remaining_requests <= 0:
                print("Limite di frequenza raggiunto. Riprova più tardi.")
                return
            '''
        # Continua con il resto del codice per ottenere le pull request
        if response.status_code == 200:
            pull_requests = response.json()
            if not pull_requests:
                break

            # da testare
            for pull_request in pull_requests:
                #print_pull_request(pull_request)

                comments = import_pull_request_comments(token, owner, repository, pull_request)
                if comments is None:
                    pull_request['comments_content'] = comments
                    return

                #print_pull_request_comments(comments)
                pull_request['comments_content'] = comments

            if temp is None:
                temp = pull_requests
            else:
                temp.extend(pull_requests)

        else:
            request_error_handler.request_error_handler(response.status_code)
            return  # Esce dalla funzione

    print(len(temp))
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
    mainTool.wait_for_rate_limit_reset(headers)
    comments_response = requests.get(comments_url, headers=headers)
    
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
    print('\n' + '-'*50 + '\n')  # Separatore per chiarezza


