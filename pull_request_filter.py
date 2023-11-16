import os
import json
from datetime import datetime

def filter_github_pull_request():
    while True:
        repository = input("\nDi quale repository vuoi filtrare le pull request? Per uscire digita esc \n")
        path = f"{repository}_data/pull_requests"

        if repository == 'esc':
            print("Uscita dalla funzione.")
            break  # Esci dal ciclo while

        if not os.path.exists(path):
            print(f"Il percorso '{path}' non esiste.")
            return

        file = input("Indica il nome del file json: ")
        path_file = f"{path}/{file}.json"

        if not os.path.exists(path_file):
            print(f"Il percorso '{path_file}' non esiste.")
            return

        status_filter = input("Inserisci lo stato delle pull requests da filtrare (es. open, closed, etc.): ")
        if not status_filter:
            print("Lo stato non è presente")
            return
        author_filter = input("Inserisci il nome dell'utente (login) da filtrare: ")
        if not author_filter:
            print("L'utente non è presente")
            return

        # Aggiungi un timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        with open(path_file, 'r', encoding='utf-8') as file:
            pull_request = json.load(file)

            filtered_pull_request = pull_request

            if status_filter:
                filtered_pull_request = [pull_request for pull_request in filtered_pull_request if pull_request.get('state') == status_filter]

            if author_filter:
                filtered_pull_request = [pull_request for pull_request in filtered_pull_request if
                                  pull_request.get('user') and pull_request['user'].get('login') == author_filter]

            filtered_pull_request_path = f"{repository}_filter_pull_request"
            os.makedirs(filtered_pull_request_path, exist_ok=True)

            # Costruisci il percorso del file JSON
            filtered_pull_request_file_path = os.path.join(filtered_pull_request_path, f'filter_pull_request_{timestamp}.json')
            with open(filtered_pull_request_file_path, 'w') as filtered_file:
                json.dump(filtered_pull_request, filtered_file, indent=4)

            print(f"Pull request filtrate salvate con successo in: {filtered_pull_request_file_path}")

# Esempio di utilizzo dello script
#filter_github_pull_request()
