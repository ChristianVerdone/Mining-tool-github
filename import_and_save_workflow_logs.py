import os
import requests
import json
from datetime import datetime
import request_error_handler

def request_github_workflows(token, owner, repository):
    api_url = f'https://api.github.com/repos/{owner}/{repository}/actions/workflows'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(api_url, headers=headers)
    return response

def request_github_workflow_runs(token, owner, repository, workflow_id):
    api_url = f'https://api.github.com/repos/{owner}/{repository}/actions/workflows/{workflow_id}/runs'
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get(api_url, headers=headers)
    return response

def get_and_save_all_github_workflow_logs(token, owner, repository):
    workflows_response = request_github_workflows(token, owner, repository)

    if workflows_response.status_code == 200:
        workflows = workflows_response.json()

        for workflow in workflows['workflows']:
            workflow_id = workflow['id']
            workflow_name = workflow['name']

            print(f"Ottenimento dei logs per il workflow: {workflow_name}")

            response = request_github_workflow_runs(token, owner, repository, workflow_id)

            if response.status_code == 200:
                workflow_runs = response.json()
                save_workflow_logs(repository, workflow_name, workflow_runs)
                print_workflow_info(workflow_runs)
            else:
                request_error_handler(response.status_code)
    else:
        request_error_handler(response.status_code)

def save_workflow_logs(repository, workflow_name, workflow_runs):
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    workflow_logs_folder = make_workflow_logs_directory(repository)
    file_path = os.path.join(workflow_logs_folder, f'{workflow_name}_logs_{timestamp}.json')

    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(workflow_runs, json_file, ensure_ascii=False, indent=4)

    print(f"I logs del workflow '{workflow_name}' sono stati salvati con successo nel file '{file_path}'")

def make_workflow_logs_directory(repository):
    repository_folder = f'{repository}_data'
    if not os.path.exists(repository_folder):
        os.makedirs(repository_folder)

    workflow_logs_folder = os.path.join(repository_folder, 'workflow_logs')
    if not os.path.exists(workflow_logs_folder):
        os.makedirs(workflow_logs_folder)

    return workflow_logs_folder

def print_workflow_info(workflow_runs):
    for run in workflow_runs['workflow_runs']:
        print(f"\nInformazioni per il run {run['run_number']}:")
        print(f"  Stato: {run['status']}")
        print(f"  Concluso: {run['conclusion']}")
        print(f"  Creato il: {run['created_at']}")
        print(f"  Durata: {run['duration'] // 60} min {run['duration'] % 60} sec")

# Esegui la funzione per ottenere e salvare i workflow logs
token = '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'  # Sostituisci con il tuo token GitHub
owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
repository = input("Inserisci il nome del repository su GitHub: ")
get_and_save_all_github_workflow_logs(token, owner, repository)