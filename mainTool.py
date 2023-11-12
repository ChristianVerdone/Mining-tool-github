import requests
import argparse

def main():
    parser = argparse.ArgumentParser(description='Un esempio di tool a riga di comando.')

    parser.add_argument('nome', nargs='?', default=None, help='Il nome per il messaggio di saluto.')
    parser.add_argument('--azione', choices=['saluta', 'calcola'], help='Azione da eseguire.')

    args = parser.parse_args()

    if args.nome is None:
        args.nome = input("Inserisci il tuo nome: ")

    if args.azione == 'saluta':
        print(f'Ciao, {args.nome}! Benvenuto nel mio tool a riga di comando.')
    elif args.azione == 'calcola':
        # Esempio di un'azione di calcolo (puoi personalizzarla in base alle tue esigenze)
        risultato = len(args.nome)
        print(f'Il risultato del calcolo sulla lunghezza del nome è: {risultato}')
    else:
        print(f'Azione non riconosciuta. Le opzioni valide sono: saluta, calcola.')

    # Replace 'owner' and 'repo_name' with the actual owner and repository name
    owner = 'owner'
    repo_name = 'repository_name'

    repo_info = get_github_repo(owner, repo_name)

    if repo_info:
        # Print the retrieved repository information
        print(f"Repository Name: {repo_info['name']}")
        print(f"Owner: {repo_info['owner']['login']}")
        print(f"Description: {repo_info['description']}")
        print(f"URL: {repo_info['html_url']}")
        # Add more fields as needed
    else:
        print("Unable to fetch repository information.")

if __name__ == '__main__':
    main()

def get_github_repo(owner, repo_name):
    base_url = 'https://api.github.com/repos'
    api_url = f'{base_url}/{owner}/{repo_name}'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer YOUR_GITHUB_TOKEN'}  # Replace with your GitHub token

    # Make the GET request to the GitHub API
    response = requests.get(api_url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        repo_info = response.json()
        return repo_info
    else:
        # Print an error message if the request was not successful
        print(f"Error: Unable to fetch repository information. Status code: {response.status_code}")
        return None