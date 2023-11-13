import requests
import json
from datetime import datetime

def print_and_save_workflow_logs():
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub per ottenere i workflow logs
    api_url = f'https://api.github.com/repos/{owner}/{repository}/actions/runs'

    # Esegui la richiesta GET all'API di GitHub Actions
    response = requests.get(api_url)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        workflow_runs = response.json()

        # Aggiungi un timestamp alle informazioni dei workflow logs
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Costruisci il nome del file JSON con il timestamp nel titolo
        file_name = f'workflow_logs_{timestamp}.json'

        # Stampa le informazioni sui workflow logs sulla console
        for run in workflow_runs['workflow_runs']:
            print(f"Workflow Run #{run['id']}:")
            print(f"  Nome: {run['name']}")
            print(f"  Stato: {run['status']}")
            print(f"  Concluso: {run['conclusion']}")
            print(f"  URL: {run['html_url']}")
            print(f"  Timestamp: {timestamp}")
            print('\n' + '-'*30 + '\n')  # Separatore per chiarezza

        # Salva le informazioni dei workflow logs in un file JSON
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(workflow_runs, json_file, ensure_ascii=False, indent=4)

        print(f"I logs dei workflow sono stati salvati con successo nel file '{file_name}'")
    else:
        print(f"Errore nella richiesta: {response.status_code}")

# Chiamare la funzione per ottenere, stampare e salvare i logs dei workflow di un repository specifico
print_and_save_workflow_logs()