from datetime import datetime
import os
import json
import requests
import mainTool
import rate_limit_handler
import request_error_handler
import rate_limit



def request_github_pull_requests(token, owner, repository, i):
    # Costruisci l'URL dell'API GitHub per ottenere le pull request
    api_url = f'https://api.github.com/repos/{owner}/{repository}/pulls?per_page=100&page={i}'
    # Utilizza il token di Github per autenticarsi
    headers = {'Authorization': 'Bearer ' + token}

    # GET request al GitHub API
    response = requests.get(api_url, headers=headers, timeout=10)

    mainTool.requests_count += 1
    rate_limit.rate_minute()
    print(f'richiesta {i}')
    rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                 response.headers['X-RateLimit-Reset'])

    return response


def github_pullreq_with_par(token):
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
        pull_requests_folder = make_pull_requests_directory(repository)
        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(pull_requests_folder, f'pull_req_{timestamp}.json')
        i = 1
        temp = None

        while True:
            response = request_github_pull_requests(token, owner, repository, i)
            i = i + 1
            if response.status_code == 200:
                # La risposta è avvenuta con successo
                pull_requests = response.json()
                if not pull_requests:
                    break

                extracted_params = extract_params_from_pullreq(pull_requests)
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
        print(f"Le informazioni sulle pull request sono state salvate con successo nel file '{file_path}'")


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


# Funzione per estrarre i parametri desiderati dalle pull requests
def extract_params_from_pullreq(pull_requests):
    # Lista per contenere solo i parametri desiderati dalle pull requests
    params_list = []
    for pull_request in pull_requests:
        extracted_params = {
            'url': pull_request['url'],
            'number': pull_request['number'],
            'title': pull_request['title'],
            'user_login': pull_request['user']['login'] if pull_request['user'] else None,
            'state': pull_request['state'],
            'assignee_login': pull_request['assignee']['login'] if pull_request['assignee'] else None,
            'body': pull_request['body']
            # Aggiungi altri parametri se necessario
        }
        params_list.append(extracted_params)
    return params_list
