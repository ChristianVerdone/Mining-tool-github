import requests

def print_github_issues():
    # Richiedi all'utente di inserire l'owner e il repository
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    # Costruisci l'URL dell'API GitHub per ottenere le issue
    api_url = f'https://api.github.com/repos/{owner}/{repository}/issues'

    # Esegui la richiesta GET all'API di GitHub
    response = requests.get(api_url)

    if response.status_code == 200:
        # La risposta è avvenuta con successo
        issues = response.json()
        # Puoi manipolare le informazioni sulle issue come desideri
        for issue in issues:
            print(f"Issue #{issue['number']}: {issue['title']} - State: {issue['state']}")

    else:
        print(f"Errore nella richiesta: {response.status_code}")

# Chiamare la funzione per ottenere e stampare le issue di un repository specifico
print_github_issues()