import requests
import argparse
import import_and_save_issue
import import_issue
import import_requests


def main():
    parser = argparse.ArgumentParser(description='Un esempio di tool a riga di comando.')

    parser.add_argument('AccessToken', nargs='?', default=None, help='Il token di accesso per API token')
    parser.add_argument('--azione', choices=['importIssue', 'ImportCommits', 'esci'], help='Azione da eseguire.')

    while True:
        args = parser.parse_args()

        if args.AccessToken is None:
            args.AccessToken = input("Inserisci il tuo Token di accesso API GitHub: ")

        if args.azione == 'importIssue':
            import_issue.print_github_issues()
        elif args.azione == 'ImportCommits':
            import_requests.fetch_github_data()
        elif args.azione == 'esci':
            print('Arrivederci!')
            break  # Esci dal loop
        else:
            print(f'Azione non riconosciuta. Le opzioni valide sono: saluta, calcola, esci.')

if __name__ == '__main__':
    main()