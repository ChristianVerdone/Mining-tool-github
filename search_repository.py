import os

import requests

import mainTool
import rate_limit
import rate_limit_handler
import request_error_handler


def controller_repo(token):
    while True:
        path = input("Indica il path del file: (Oppure esci) ")
        if path == 'esci':
            break

        if not os.path.exists(path):
            print(f"Il percorso '{path}' non esiste ")
            break

        file = input("Inserisci il nome del file txt: ")
        path_file = f"{path}/{file}.txt"

        if not os.path.exists(path_file):
            print(f"Il percorso '{path_file}' non esiste.")
            break

        # Lista per memorizzare i repository trovati
        repositories_found = []

        # Leggi da file .txt l'owner/repository
        with open(path_file, 'r', encoding='utf-8') as file:
            # Per ogni riga del file prendi l'owner e il repository
            lines = file.readlines()
            for line in lines:

                owner, repository = line.strip().split('/')  # Assume che il formato sia 'owner/repository'

                response = request_github(token, owner, repository)
                # print(f"Errore: '{response.status_code}")

                mainTool.requests_count += 1
                rate_limit.rate_minute()

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
        with open('repo.txt', 'w', encoding='utf-8') as repo_file:
            for repo in repositories_found:
                repo_file.write(f"{repo}\n")


def request_github(token, owner, repository):
    # Costruisci l'URL dell'API GitHub
    api_url = f'https://api.github.com/repos/{owner}/{repository}'
    # Utilizza il token di Github per autenticarsi
    headers = {'Authorization': 'Bearer ' + token}
    # GET request al GitHub API
    # timeout=10 specifica che la richiesta HTTP si interromperà dopo 30 secondi se non viene ricevuta una risposta.
    response = requests.get(api_url, headers=headers, timeout=30)
    rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                 response.headers['X-RateLimit-Reset'])
    return response
