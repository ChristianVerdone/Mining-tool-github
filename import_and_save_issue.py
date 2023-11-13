import requests
import json


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

        # Stampa le informazioni sulle issue sulla console
        for issue in issues:
            print(f"Issue #{issue['number']}:")
            print(f"  Titolo: {issue['title']}")
            print(f"  Stato: {issue['state']}")
            print(f"  Autore: {issue['user']['login']}")
            print(f"  URL: {issue['html_url']}")
            print('\n' + '-'*30 + '\n')  # Separatore per chiarezza

        # Salva le informazioni delle issue in un file JSON
        with open('issues.json', 'w', encoding='utf-8') as json_file:
            json.dump(issues, json_file, ensure_ascii=False, indent=4)

        print(f"Le informazioni delle issue sono state salvate con successo nel file 'issues.json'")
    else:
        print(f"Errore nella richiesta: {response.status_code}")
