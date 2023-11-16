import os
import requests
import os
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

        # Crea una directory per i log dei flussi di lavoro
        workflow_dir = os.path.join(repository, "workflow_logs")
        os.makedirs(workflow_dir, exist_ok=True)

        # Aggiungi un timestamp alle informazioni dei workflow logs
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Creare la cartella principale con il nome del repository
        repository_folder = f'{repository}_data'
        if not os.path.exists(repository_folder):
            os.makedirs(repository_folder)

        # Creare la sottocartella con il nome "workflow_logs"
        workflow_logs_folder = os.path.join(repository_folder, 'workflow_logs')
        if not os.path.exists(workflow_logs_folder):
            os.makedirs(workflow_logs_folder)

        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(workflow_logs_folder, f'workflow_logs_{timestamp}.json')

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
        # Salva i dati localmente (esempio: in un file JSON)
        log_file_path = os.path.join(workflow_dir, file_name)
        with open(log_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(workflow_runs, json_file, ensure_ascii=False, indent=4)

        print(f"I logs dei workflow sono stati salvati con successo nel file '{file_path}'")
    else:
        print(f"Errore nella richiesta: {response.status_code}")

# Chiamare la funzione per ottenere, stampare e salvare i logs dei workflow di un repository specifico
print_and_save_workflow_logs()