import os
import requests
import json
from datetime import datetime


def print_and_save_github_issues(token):
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer '+token}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        issues = response.json()

        # Aggiungi un timestamp alle informazioni delle issue
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Creare la cartella principale con il nome del repository
        repository_folder = f'{repository}_data'
        if not os.path.exists(repository_folder):
            os.makedirs(repository_folder)

        # Creare la sottocartella con il nome "issues"
        issues_folder = os.path.join(repository_folder, 'issues')
        if not os.path.exists(issues_folder):
            os.makedirs(issues_folder)

        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(issues_folder, f'issues_with_comments_{timestamp}.json')

        # Stampa le informazioni sulle issue e i relativi commenti sulla console
        for issue in issues:
            print(f"Issue #{issue['number']}:")
            print(f"  Titolo: {issue['title']}")
            print(f"  Stato: {issue['state']}")
            print(f"  URL: {issue['html_url']}")

            # Ottieni i commenti della issue
            comments_url = f'https://api.github.com/repos/{owner}/{repository}/issues/{issue["number"]}/comments'
            comments_response = requests.get(comments_url)
            comments = comments_response.json()

            # Stampa i commenti
            print("  Commenti:")
            for comment in comments:
                print(f"    {comment['user']['login']}: {comment['body']}")

            print('\n' + '-'*30 + '\n')  # Separatore per chiarezza

        # Salva le informazioni delle issue e dei commenti in un file JSON
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(issues, json_file, ensure_ascii=False, indent=4)

        print(f"Le informazioni delle issue sono state salvate con successo nel file '{file_path}'")
    else:
        print(f"Errore nella richiesta: {response.status_code}")

