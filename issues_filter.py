import os
import json

def filter_github_issues():
    while True:
        repository = input("\nDi quale repository vuoi filtrare le issues? Per uscire digita esc \n")
        path = f"{repository}_data/issues"
        
        if repository == 'esc':
            print("Uscita dalla funzione.")
            break  # Esci dal ciclo while

        if not os.path.exists(path):
            print(f"Il percorso '{path}' non esiste.")
            return
        
        file = input("Indica il nome del file json: ")
        path_file=f"{path}/{file}.json"

        if not os.path.exists(path_file):
            print(f"Il percorso '{path_file}' non esiste.")
            return

        status_filter = input("Inserisci lo stato delle issue da filtrare (es. open, closed, etc.): ")
        if not status_filter:
            print("Lo stato non è presente")
            return
        author_filter = input("Inserisci il nome dell'utente (login) delle issue da filtrare: ")
        if not author_filter:
            print("L'utente non è presente")
            return

        with open(path_file, 'r') as file:
            issues = json.load(file)

            filtered_issues = issues

            if status_filter:
                filtered_issues = [issue for issue in filtered_issues if issue.get('state') == status_filter]

            if author_filter:
                filtered_issues = [issue for issue in filtered_issues if issue.get('user') and issue['user'].get('login') == author_filter]

            filtered_issues_path = f"{repository}_filter_issues"
            os.makedirs(filtered_issues_path, exist_ok=True)

            filtered_issues_file_path = os.path.join(filtered_issues_path, "filter_issues.json")
            with open(filtered_issues_file_path, 'w') as filtered_file:
                json.dump(filtered_issues, filtered_file, indent=4)

            print(f"Issue filtrate salvate con successo in: {filtered_issues_file_path}")

# Esempio di utilizzo dello script
filter_github_issues()
