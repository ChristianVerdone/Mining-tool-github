import os
import json
import requests
import mainTool
import rate_limit_handler
import request_error_handler
import rate_limit
from datetime import datetime


def request_github_issues(token, owner, repository, i):
    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues?per_page=100&page={i}'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer ' + token}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    mainTool.requests_count += 1
    rate_limit.rate_minute()
    rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                 response.headers['X-RateLimit-Reset'])

    print(f'richiesta {i}')
    return response


def github_issues_with_par(token):
    
    while True:
        # Richiedi all'utente di inserire l'owner e il repository
        owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
        repository = input("Inserisci il nome del repository su GitHub: ")

        if repository == 'esci' or owner == 'esci':
            print("Uscita dalla funzione.")
            break  # Esci dal ciclo while
        
        # Aggiungi un timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Creiamo la directory
        issues_folder = make_issues_directory(repository)
        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(issues_folder, f'issues_with_parameters_{timestamp}.json')
        i = 1
        temp = None
        while True:
            response = request_github_issues(token, owner, repository, i)
            i = i + 1
            if response.status_code == 200:
                # La risposta è avvenuta con successo
                issues = response.json()
                # Se l'oggetto json issues è vuoto allora esco dal ciclo perchè ho raggiunto la fine degli elementi da collezionare
                if not issues:
                    break

                extracted_params = extract_params_from_issues(issues)
            else:
                request_error_handler.request_error_handler(response.status_code)
                return
            # alla prima iterazione temp sarà None e lo rendo un oggetto json assegnando il valore di issues
            if temp is None:
                temp = extracted_params   
            # altrimenti inserisco in coda a temp gli elementi delle issues successive
            else:
                temp.extend(extracted_params) 

        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(temp, json_file, ensure_ascii=False, indent=4)
        print(f"Le informazioni delle issue sono state salvate con successo nel file '{file_path}'")


def make_issues_directory(repository):
    # Creare la cartella principale con il nome del repository
    repository_folder = f'{repository}_data'
    if not os.path.exists(repository_folder):
        os.makedirs(repository_folder)

    # Creare la sottocartella con il nome "issues"
    issues_folder = os.path.join(repository_folder, 'issues')
    if not os.path.exists(issues_folder):
        os.makedirs(issues_folder)

    return issues_folder


# Funzione per estrarre i parametri desiderati dalle issues
def extract_params_from_issues(issues):
    # Lista per contenere solo i parametri desiderati dalle issues
    params_list = []
    for issue in issues:
        extracted_params = {
            'url': issue['url'],
            'number': issue['number'],
            'title': issue['title'],
            'user_login': issue['user']['login'] if issue['user'] else None,
            'state': issue['state'],
            'assignee_login': issue['assignee']['login'] if issue['assignee'] else None,
            'comments': issue['comments']
            # Aggiungi altri parametri se necessario
        }
        params_list.append(extracted_params)
    return params_list
