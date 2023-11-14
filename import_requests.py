import requests


def fetch_github_data(token):
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub utilizzando i valori inseriti dall'utente
    api_url = f'https://api.github.com/repos/{owner}/{repository}/commits'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer '+token}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        data = response.json()
        # Puoi manipolare i dati come desideri
        for commit in data:
            print(commit['commit']['author']['name'], commit['commit']['message'])
    else:
        print(f"Errore nella richiesta: {response.status_code}")

