
import os
import requests
import json
from datetime import datetime

import request_error_handler
import rate_limit_handler


def save_github_workflow_logs(token):

    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Aggiungi un timestamp alle informazioni dei workflow logs
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    workflow_logs_folder = make_workflow_logs_directory(repository)
    # Costruisci il percorso del file JSON con il timestamp nel titolo
    file_path = os.path.join(workflow_logs_folder, f'workflow_logs_{timestamp}.json')
    
    i = 1
    temp = None
    
    while True:
        response = get_github_workflow_logs(token, owner, repository, i)
        i = i + 1
        if response.status_code == 200:
        # La risposta è avvenuta con successo
            workflow_runs = response.json()
            
            if not workflow_runs:
                break
            
            for run in workflow_runs['workflow_runs']:
                print_workflow_info(run)
                
            if temp is None:
                temp = workflow_runs
            else:
                temp['workflow_runs'].extend(workflow_runs['workflow_runs'])
            
        else:
            request_error_handler.request_error_handler(response.status_code)
            print("Errore nel recupero dei workflow logs.")
            return

    # Salva le informazioni dei workflow logs in un file JSON
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(temp, json_file, ensure_ascii=False, indent=4)
    print(f"I logs dei workflow sono stati salvati con successo nel file '{file_path}'")
    

def get_github_workflow_logs(token, owner, repository, i):
    # Ottieni i workflow logs
    api_url = f'https://api.github.com/repos/{owner}/{repository}/actions/runs?per_page=100&page={i}'
    headers = {'Authorization': 'Bearer ' + token}
    
    rate_limit_handler.wait_for_rate_limit_reset(headers)
    
    response = requests.get(api_url, headers=headers)
    
    print(f'richiesta {i}')

    return response


def print_workflow_info(run):
    # Stampa le informazioni sui workflow logs sulla console
    print(f"Workflow Run #{run['id']}:")
    print(f"  Nome: {run['name']}")
    print(f"  Stato: {run['status']}")
    print(f"  Concluso: {run['conclusion']}")
    print(f"  URL: {run['html_url']}")
    print('\n' + '-'*30 + '\n')  # Separatore per chiarezza


def make_workflow_logs_directory(repository):
    # Creare la cartella principale con il nome del repository
    repository_folder = f'{repository}_data'
    if not os.path.exists(repository_folder):
        os.makedirs(repository_folder)

    # Creare la sottocartella con il nome "workflow_logs"
    workflow_logs_folder = os.path.join(repository_folder, 'workflow_logs')
    if not os.path.exists(workflow_logs_folder):
        os.makedirs(workflow_logs_folder)

    return workflow_logs_folder

# Esempio di utilizzo
  # Sostituisci con il tuo token GitHub
#save_github_workflow_logs(token)