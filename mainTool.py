import argparse
import requests
import issue_handler
import import_pull_requests
import import_and_save_workflow_logs
from issues_filter import filter_github_issues
import request_error_handler


def main():
    parser = argparse.ArgumentParser(description='Un esempio di tool a riga di comando.')

    parser.add_argument('AccessToken', nargs='?', default=None, help='Il token di accesso per API token')
    parser.add_argument('--azione', choices=['importIssue', 'importPullrequests', 'importWorkflowlogs'
                                             'esci', 'newAuth', 'filterOutputIssue'], help='Azione da eseguire.')

    args = parser.parse_args()
    auth = False
    while True:
        if not auth:
            if args.AccessToken is None:
                args.AccessToken = input("Benvenut*, Inserisci il tuo Token di accesso API GitHub: ")
                # Imposta l'intestazione con il token di accesso
                headers = {
                    'Authorization': f'token {args.AccessToken}',
                    'Accept': 'application/vnd.github.v3+json'
                }

                # richiesta GET a GitHub API
                url = 'https://api.github.com/user'
                response = requests.get(url, headers=headers)

                # Gestisci la risposta
                if response.status_code == 200:
                    print("Richiesta riuscita!")
                    user = response.json()
                    print("Benvenut* :" + user['login'] + '\n Questo è il nuovo tool di mining per GitHub. Le azioni consentite sono:'
                          '\n --azione importIssue'
                          '\n --azione importPullrequests'
                          '\n --azione importWorkflowlogs'
                          '\n --azione newAuth'
                          '\n --azione filterOutputIssue'
                          '\n --azione esci ')
                    auth = True

                else:
                    request_error_handler.request_error_handler(response.status_code)
                    print("Assicurati di aver inserito il token correttamente o che sia ancora valido per accedere all'API\n")
                    args.AccessToken = None

        if auth:
            if args.azione is None:
                args.azione = input("Inserisci l'azione che desideri effettuare: ")

            if args.azione == 'importIssue':
                issue_handler.save_github_issues(args.AccessToken)
                args.azione = None
            elif args.azione == 'importPullrequests':
                import_pull_requests.save_github_pull_requests(args.AccessToken)
                args.azione = None
            elif args.azione == 'importWorkflowlogs':
                import_and_save_workflow_logs.import_and_save_workflow_logs(args.AccessToken)
                args.azione = None    
            elif args.azione == 'esci':
                print('Arrivederci!')
                break  # Esci dal loop
            elif args.azione == 'newAuth':
                args.azione = None
                args.AccessToken = None
                auth = False
            elif args.azione == 'filterOutputIssue':
                filter_github_issues()
                args.azione = None
            else:
                print(f'Azione non riconosciuta. Le opzioni valide sono: importIssue, importPullrequests, importWorkflowlogs, newAuth, filterOutputIssue, esci')
                args.azione = None


if __name__ == '__main__':
    main()
