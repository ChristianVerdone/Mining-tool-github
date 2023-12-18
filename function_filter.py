import os
import json
from datetime import datetime


def filter_github():
    scelta = input('Filtrare per repository o path: ')
    scelta_i_pr = input("Filtrare issues o pull_request: ")

    if scelta == 'path':
        if scelta_i_pr == 'issues':
            while True:
                path = input("\nIndica il percorso (Per uscire digita esc) ")
                if path == 'esc':
                    print("Uscita dalla funzione.")
                    break  # Esci dal ciclo while

                path_file = f_path(path)

                status_filter = state()
                author_filter = user_login()

                filtered_issues_file_path = filter_issues_by_path(path_file, status_filter, author_filter)
                print(f"Issue filtrate salvate con successo in: {filtered_issues_file_path}")

        elif scelta_i_pr == 'pull_request':
            while True:
                path = input("\nInserisci il percorso: (Per uscire digita esc)")
                if path == 'esc':
                    print("Uscita dalla funzione.")
                    break  # Esci dal ciclo while

                path_file = f_path(path)

                status_filter = state()
                author_filter = user_login()

                filtered_pr_file_path = filter_pull_request_by_path(path_file, status_filter, author_filter)
                print(f"Pull request filtrate salvate con successo in: {filtered_pr_file_path}")
        return
    elif scelta == 'repository':
        if scelta_i_pr == 'issues':
            while True:
                repository = input("\nIndica il repository (Per uscire digita esc) ")
                if repository == 'esc':
                    print("Uscita dalla funzione.")
                    break  # Esci dal ciclo while

                path = f"{repository}_data/issues"

                path_file = f_path(path)

                status_filter = state()
                author_filter = user_login()

                filtered_issues_file_path = filter_github_issues(repository, path_file, status_filter, author_filter)
                print(f"Issue filtrate salvate con successo in: {filtered_issues_file_path}")

        elif scelta_i_pr == 'pull_request':
            while True:
                repository = input("\nIndica il repository (Per uscire digita esc) \n")
                if repository == 'esc':
                    print("Uscita dalla funzione.")
                    break  # Esci dal ciclo while

                path = f"{repository}_data/pull_requests"

                path_file = f_path(path)

                status_filter = state()
                author_filter = user_login()

                filtered_pr_file_path = filter_github_pull_request(repository, path_file, status_filter, author_filter)
                print(f"Pull request filtrate salvate con successo in: {filtered_pr_file_path}")

    return


def filter_issues_by_path(path_file, status_filter, author_filter):
    status_filter = status_filter
    author_filter = author_filter

    with open(path_file, 'r', encoding='utf-8') as file:
        issues = json.load(file)
        filtered_issues = issues

        if status_filter:
            filtered_issues = [issue for issue in filtered_issues if issue.get('state') == status_filter]

        if author_filter:
            filtered_issues = [issue for issue in filtered_issues if
                               issue.get('user') and issue['user'].get('login') == author_filter]

        filtered_issues_path = "issues_by_path"
        filtered_issues_file_path = create_folder(filtered_issues_path, filtered_issues)

    return filtered_issues_file_path


def filter_pull_request_by_path(path_file, status_filter, author_filter):
    status_filter = status_filter
    author_filter = author_filter

    with open(path_file, 'r', encoding='utf-8') as file:
        pull_request = json.load(file)
        filtered_pull_request = pull_request

        if status_filter:
            filtered_pull_request = [pull_request for pull_request in filtered_pull_request if
                                     pull_request.get('state') == status_filter]

        if author_filter:
            filtered_pull_request = [pull_request for pull_request in filtered_pull_request if
                                     pull_request.get('user') and pull_request['user'].get('login') == author_filter]

        filtered_pull_request_path = "p_req_by_path"
        filtered_pr_file_path = create_folder(filtered_pull_request_path, filtered_pull_request)

    return filtered_pr_file_path


def filter_github_issues(repository, path_file, status_filter, author_filter):
    status_filter = status_filter
    author_filter = author_filter

    with open(path_file, 'r', encoding='utf-8') as file:
        issues = json.load(file)
        filtered_issues = issues

        if status_filter:
            filtered_issues = [issue for issue in filtered_issues if issue.get('state') == status_filter]

        if author_filter:
            filtered_issues = [issue for issue in filtered_issues if
                               issue.get('user') and issue['user'].get('login') == author_filter]

        filtered_issues_path = f"{repository}_filter_issues"
        filtered_issues_file_path = create_folder(filtered_issues_path, filtered_issues)

    return filtered_issues_file_path


def filter_github_pull_request(repository, path_file, status_filter, author_filter):
    status_filter = status_filter
    author_filter = author_filter

    with open(path_file, 'r', encoding='utf-8') as file:
        pull_request = json.load(file)
        filtered_pull_request = pull_request

        if status_filter:
            filtered_pull_request = [pull_request for pull_request in filtered_pull_request if
                                     pull_request.get('state') == status_filter]

        if author_filter:
            filtered_pull_request = [pull_request for pull_request in filtered_pull_request if
                                     pull_request.get('user') and pull_request['user'].get('login') == author_filter]

        filtered_pull_request_path = f"{repository}_filter_pull_request"
        filtered_pr_file_path = create_folder(filtered_pull_request_path, filtered_pull_request)

    return filtered_pr_file_path


def create_folder(folder_path, filter):
    os.makedirs(folder_path, exist_ok=True)
    # Aggiungi un timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Costruisci il percorso del file JSON
    filtered_file_path = os.path.join(folder_path, f'filter_issues_{timestamp}.json')
    with open(filtered_file_path, 'w') as filtered_file:
        json.dump(filter, filtered_file, indent=4)

    return filtered_file_path


def f_path(path):
    if not os.path.exists(path):
        print(f"Il percorso '{path}' non esiste ")
        return

    file = input("Inserisci il nome del file json: ")
    # path_file = f"{path}\{file}.json"
    path_file = os.path.join(path, f"{file}.json")

    if not os.path.exists(path_file):
        print(f"Il percorso '{path_file}' non esiste.")
        return

    return path_file


def state():
    status_filter = input("Indica lo stato da filtrare (es. open, closed, etc.): ")
    if not status_filter:
        print("Lo stato non è presente")
        return
    return status_filter


def user_login():
    author_filter = input("Indica lo user (login) da filtrare: ")
    if not author_filter:
        print("L'utente non è presente")
        return

    return author_filter
