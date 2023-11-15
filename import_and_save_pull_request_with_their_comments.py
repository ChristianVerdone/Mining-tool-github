import os
import requests
import json
from datetime import datetime


def print_and_save_pull_requests_with_comments(token):
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub per ottenere le pull requests
    api_url = f'https://api.github.com/repos/{owner}/{repository}/pulls'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer ' + token}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        pull_requests = response.json()

        # Aggiungi un timestamp alle informazioni delle pull requests
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Creare la cartella principale con il nome del repository
        repository_folder = f'{repository}_data'
        if not os.path.exists(repository_folder):
            os.makedirs(repository_folder)

        # Creare la sottocartella con il nome "pull_requests"
        pull_requests_folder = os.path.join(repository_folder, 'pull_requests')
        if not os.path.exists(pull_requests_folder):
            os.makedirs(pull_requests_folder)

        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(pull_requests_folder, f'pull_requests_with_comments_{timestamp}.json')

        # Stampa le informazioni sulle pull requests e i relativi commenti sulla console
        for pull_request in pull_requests:
            print(f"Pull Request #{pull_request['number']}:")
            print(f"  Titolo: {pull_request['title']}")
            print(f"  Stato: {pull_request['state']}")
            print(f"  URL: {pull_request['html_url']}")

            # Ottieni i commenti della pull request
            comments_url = f'https://api.github.com/repos/{owner}/{repository}/issues/{pull_request["number"]}/comments'
            comments_response = requests.get(comments_url)
            comments = comments_response.json()

            # Stampa i commenti
            print("  Commenti:")
            for comment in comments:
                print(f"    {comment['user']['login']}: {comment['body']}")

            print('\n' + '-'*30 + '\n')  # Separatore per chiarezza

        # Salva le informazioni delle pull requests e dei commenti in un file JSON
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(pull_requests, json_file, ensure_ascii=False, indent=4)

        print(f"Le informazioni delle pull requests sono state salvate con successo nel file '{file_path}'")
    else:
        print(f"Errore nella richiesta: {response.status_code}")


# Chiamare la funzione per ottenere, stampare e salvare le pull requests con i relativi commenti di un repository specifico
print_and_save_pull_requests_with_comments()