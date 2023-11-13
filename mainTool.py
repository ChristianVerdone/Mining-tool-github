import requests
import argparse


def main():
    parser = argparse.ArgumentParser(description='Un esempio di tool a riga di comando.')

    parser.add_argument('AccessToken', nargs='?', default=None, help='Il token di accesso per API token')
    parser.add_argument('--azione', choices=['importIssue', 'ImportCommits'], help='Azione da eseguire.')

    while True:
        args = parser.parse_args()

        if args.nome is None:
            args.nome = input("Inserisci il tuo Token di accesso API GitHub: ")

        if args.azione == 'importIssue':
            print(f'Ciao, {args.nome}! Benvenuto nel mio tool a riga di comando.')
        elif args.azione == 'calcola':
            risultato = len(args.nome)
            print(f'Il risultato del calcolo sulla lunghezza del nome è: {risultato}')
        elif args.azione == 'esci':
            print('Arrivederci!')
            break  # Esci dal loop
        else:
            print(f'Azione non riconosciuta. Le opzioni valide sono: saluta, calcola, esci.')

if __name__ == '__main__':
    main()


def get_github_repo(owner, repo_name):
    base_url = 'https://api.github.com/repos'
    api_url = f'{base_url}/{owner}/{repo_name}'

    # Provide your GitHub API token if you have one
    headers = {'Authorization': 'Bearer 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'}  # Replace with your GitHub token

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
