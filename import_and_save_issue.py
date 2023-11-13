import requests
import json
from datetime import datetime

def print_and_save_github_issues():
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues'

    # Esegui la richiesta GET all'API di GitHub
    response = requests.get(api_url)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        issues = response.json()

        # Aggiungi un timestamp alle informazioni delle issue
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        for issue in issues:
            issue['timestamp'] = timestamp

        # Costruisci il nome del file JSON con il timestamp nel titolo
        file_name = f'issues_{timestamp}.json'

        # Stampa le informazioni sulle issue sulla console
        for issue in issues:
            print(f"Issue #{issue['number']}:")
            print(f"  Titolo: {issue['title']}")
            print(f"  Stato: {issue['state']}")
            print(f"  Autore: {issue['user']['login']}")
            print(f"  URL: {issue['html_url']}")
            print(f"  Timestamp: {issue['timestamp']}")
            print('\n' + '-'*30 + '\n')  # Separatore per chiarezza

        # Salva le informazioni delle issue in un file JSON
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(issues, json_file, ensure_ascii=False, indent=4)

        print(f"Le informazioni delle issue sono state salvate con successo nel file '{file_name}'")
    else:
        print(f"Errore nella richiesta: {response.status_code}")

# Chiamare la funzione per ottenere, stampare e salvare le issue di un repository specifico
print_and_save_github_issues()