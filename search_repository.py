import os
import requests
import request_error_handler

def controller_repo(token):
    path=input("Indica il path del file: ")
    path_file=f_path_txt(path)
    
    #Leggi da file .txt l'owner/repository
    with open(path_file, 'r') as file:
        #Per ogni riga del file prendi l'owner e il repository 
        lines = file.readlines()
        for line in lines:
            owner, repository = line.strip().split('/')  # Assume che il formato sia 'owner/repository'

            response = request_github(token, owner, repository)
            if response.status_code == 200:
                print(f'{owner}/{repository}')
            else:
                # Il repository non è stato trovato
                print(f"'{owner}/{repository}' (NOT Found)")
            '''elif response.status_code == 404:
                # Il repository non è stato trovato
                print(f"'{owner}/{repository}' (NOT Found)")
            else:
                # Gestione degli altri possibili errori
                request_error_handler.request_error_handler(response.status_code)
            '''

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
        
    file=input("Inserisci il nome del file txt: ")
    path_file=f"{path}/{file}.txt"

    if not os.path.exists(path_file):
        print(f"Il percorso '{path_file}' non esiste.")
        return
    return path_file       


   
