import requests


def print_github_issues(token):
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer '+token}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        issues = response.json()
        # Puoi manipolare le informazioni sulle issue come desideri
        for issue in issues:
            print(f"Issue #{issue['number']}: {issue['title']} - State: {issue['state']}")

    else:
        print(f"Errore nella richiesta: {response.status_code}")
