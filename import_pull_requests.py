import os
import requests
import json
import request_error_handler
from datetime import datetime


def request_github_pull_requests(token, owner, repository):

    # Costruisci l'URL dell'API GitHub per ottenere le pull request
    api_url = f'https://api.github.com/repos/{owner}/{repository}/pulls'

    # Utilizza il token di Github per autenticarsi 
    headers = {'Authorization': 'Bearer ' + token}

     # GET request al GitHub API
    response = requests.get(api_url, headers=headers)

    return response


# Salva le pull request passando il token come parametro
def save_github_pull_requests(token):

    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    response = request_github_pull_requests(token, owner, repository)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        pull_requests = response.json()

        # Aggiungi un timestamp alle informazioni delle pull request
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        pull_requests_folder = make_pull_requests_directory(repository)

        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(pull_requests_folder, f'pull_requests_{timestamp}.json')

        for pull_request in pull_requests:
            print_pull_request(pull_request)
            
            comments = import_pull_request_comments(owner, repository, pull_request)
            #check comments request
            if comments is None:
                return
            
            print_pull_request_comments(comments)
            pull_request['comments_content'] = comments

        # Salva le informazioni delle issue e dei commenti in un file JSON
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(pull_requests, json_file, ensure_ascii=False, indent=4)

        print(f"Le informazioni sulle pull request sono state salvate con successo nel file '{file_path}'")
    else:
        request_error_handler(response.status_code)
        return #esce dalla funzione


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


def import_pull_request_comments(owner, repository, pull_request):
    # Ottieni i commenti delle pull request
    comments_url = f'https://api.github.com/repos/{owner}/{repository}/pulls/{pull_request["number"]}/comments'
    comments_response = requests.get(comments_url)
    
    if(comments_response.status_code != 200):
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
    print('\n' + '-'*30 + '\n') # Separatore per chiarezza

