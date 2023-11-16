import os
import requests
import json
import request_error_handler
from datetime import datetime

def request_github_issues(token, owner, repository):

    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer '+token}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)
    
    return response


def save_github_issues(token):
    
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")
    
    response = request_github_issues(token, owner, repository)
    
    if response.status_code == 200:
        # La risposta è avvenuta con successo
        issues = response.json()

        # Aggiungi un timestamp alle informazioni delle issue
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        issues_folder = make_issues_directory(repository)

        # Costruisci il percorso del file JSON con il timestamp nel titolo
        file_path = os.path.join(issues_folder, f'issues_with_comments_{timestamp}.json')
        
        for issue in issues:
            print_issue(issue)
            comments = import_issue_comments(owner, repository, issue)
            print_issue_comments(comments)
            if comments:
                 issue['comments_content'] = comments
            
        # Salva le informazioni delle issue e dei commenti in un file JSON
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(issues, json_file, ensure_ascii=False, indent=4)
        
        print(f"Le informazioni delle issue sono state salvate con successo nel file '{file_path}'")     
    else:
        request_error_handler(response.status_code)
        return  #esci dalla funzione 
        
        
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
    
        
def import_issue_comments(owner, repository, issue):
    # Ottieni i commenti della issue
    comments_url = f'https://api.github.com/repos/{owner}/{repository}/issues/{issue["number"]}/comments'
    comments_response = requests.get(comments_url)
    
    if(comments_response != 200):
        request_error_handler(comments_response.status_code)
        comments = None
        return comments
        #controllare se comments vuoto vale none oppure diversamente...
    
    comments = comments_response.json()
    
    return comments
    

def print_issue(issue):
    # Stampa le informazioni sulle issue e i relativi commenti sulla console
        print(f"Issue #{issue['number']}:")
        print(f"  Titolo: {issue['title']}")
        print(f"  Stato: {issue['state']}")
        print(f"  URL: {issue['html_url']}")
        
        
def print_issue_comments(comments):
    # Stampa i commenti
        print("  Commenti:")
        for comment in comments:
            print(f"    {comment['user']['login']}: {comment['body']}")

        print('\n' + '-'*30 + '\n')  # Separatore per chiarezza