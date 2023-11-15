import argparse

import import_and_save_issue
import import_and_save_pull_request_with_their_comments
import import_issue
import import_requests


def main():
    parser = argparse.ArgumentParser(description='Un esempio di tool a riga di comando.')

    parser.add_argument('AccessToken', nargs='?', default=None, help='Il token di accesso per API token')
    parser.add_argument('--azione', choices=['importIssue', 'importCommits', 'import_saveIssue', 'import_PullRequests', 'esci'], help='Azione da eseguire.')

    print('Benvenut* nel nuovo tool di mining per GitHub. Le azioni consentite sono:'
          '--azione importIssue'
          '--azione importCommits'
          '--azione import_saveIssue'
          '--azione esci ')
    args = parser.parse_args()
    while True:

        if args.AccessToken is None:
            args.AccessToken = input("Inserisci il tuo Token di accesso API GitHub: ")

        if args.azione is None:
            args.azione = input("Inserisci l'azione che desideri effettuare: ")

        if args.azione == 'importIssue':
            import_issue.print_github_issues(args.AccessToken)
            args.azione = None
        elif args.azione == 'importCommits':
            import_requests.fetch_github_data(args.AccessToken)
            args.azione = None
        elif args.azione == 'import_saveIssue':
            import_and_save_issue.print_and_save_github_issues(args.AccessToken)
            args.azione = None
        elif args.azione == 'import_PullRequests':
            import_and_save_pull_request_with_their_comments.print_and_save_pull_requests_with_comments(args.AccessToken)
            args.azione = None
        elif args.azione == 'esci':
            print('Arrivederci!')
            break  # Esci dal loop
        else:
            print(f'Azione non riconosciuta. Le opzioni valide sono: saluta, calcola, esci.')
            args.azione = None

if __name__ == '__main__':
    main()
