import os
import requests
import request_error_handler
import rate_limit
import time


def controller_repo(token):
    path = input("Indica il path del file: ")
    path_file = f_path_txt(path)

    start_time= time.time()
    request_count = 0
    
    # Lista per memorizzare i repository trovati
    repositories_found = []
    
    # Leggi da file .txt l'owner/repository
    with open(path_file, 'r') as file:
        # Per ogni riga del file prendi l'owner e il repository
        lines = file.readlines()
        for line in lines:

            request_count += 1
            rate_limit.rate_minute(start_time, request_count)

            owner, repository = line.strip().split('/')  # Assume che il formato sia 'owner/repository'

            response = request_github(token, owner, repository)
            #print(f"Errore: '{response.status_code}")

            if response.status_code == 200:
                # Aggiungi il repository alla lista dei repository trovati
                repositories_found.append(f'{owner}/{repository}')
                # print(f'{owner}/{repository}')
            
            elif response.status_code == 404:
                # Il repository non è stato trovato
                print(f"'{owner}/{repository}' (NOT Found)")
            else:
                # Gestione degli altri possibili errori
                request_error_handler.request_error_handler(response.status_code)
            
    
    # Scrivo i repository trovati nel file 'repo.txt'
    with open('repo.txt', 'w') as repo_file:
        for repo in repositories_found:
            repo_file.write(f"{repo}\n")        
            
            


def request_github(token, owner, repository):
    # Costruisci l'URL dell'API GitHub
    api_url = f'https://api.github.com/repos/{owner}/{repository}'
    # Utilizza il token di Github per autenticarsi
    headers = {'Authorization': 'Bearer ' + token}
    # GET request al GitHub API
    response = requests.get(api_url, headers=headers)

    return response


def f_path_txt(path):
    if not os.path.exists(path):
        print(f"Il percorso '{path}' non esiste ")
        return

    file = input("Inserisci il nome del file txt: ")
    path_file = f"{path}/{file}.txt"

    if not os.path.exists(path_file):
        print(f"Il percorso '{path_file}' non esiste.")
        return
    return path_file
