import argparse
import os

import requests

import import_and_save_workflow_logs
import import_issue_without_comments
import import_pull_request_without_comments
import import_pull_requests
import issue_handler
import rate_limit
import rate_limit_handler
import request_error_handler
import search_repository
from function_filter import filter_github
from issues_with_parameters import github_issues_with_par
from pull_req_with_parameters import github_pullreq_with_par

# global start_time
start_time = 0
requests_count = 0


def main():
    global requests_count
    parser = argparse.ArgumentParser(description='tool di Mining a riga di comando.')

    parser.add_argument('AccessToken', nargs='?', default=None, help='Il token di accesso per API token')
    parser.add_argument('--a', choices=['importIssue', 'importPullrequests', 'importWorkflowlogs', 'esci',
                                        'newAuth', 'filterOutput', 'search_repo', 'importPullrequestswithoutcomments',
                                        'importIssuewithoutcomments', 'issuesWithParameters', 'pullReqWithParameters'],
                        help='Azione da eseguire.')

    args = parser.parse_args()
    auth = False

    if os.path.exists('auth.txt'):
        with open('auth.txt', 'r') as file:
            temp = file.readline()
            # Imposta l'intestazione con il token di accesso
            headers = {
                'Authorization': f'token {temp}',
                'Accept': 'application/vnd.github.v3+json'
            }
            # richiesta GET a GitHub API
            url = 'https://api.github.com/user'
            response = requests.get(url, headers=headers)

            requests_count += 1
            rate_limit.rate_minute()
            rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                         response.headers['X-RateLimit-Reset'])
            # Gestisci la risposta
            if response.status_code == 200:
                args.AccessToken = temp
                auth = True
                user = response.json()
                print("Benvenut* :" + user['login'] +
                      '\n Questo è il nuovo tool di mining per GitHub. Le azioni consentite sono:'
                      '\n --a importIssue'
                      '\n --a importPullrequests'
                      '\n --a importWorkflowlogs'
                      '\n --a newAuth'
                      '\n --a filterOutput'
                      '\n --a search_repo'
                      '\n --a importPullrequestswithoutcomments'
                      '\n --a importIssuewithoutcomments'
                      '\n --a issuesWithParameters'
                      '\n --a pullReqWithParameters'
                      '\n --a esci ')
            else:
                print(
                    "Non è stato possibile recuperare il token dal file di inizializzazione, si prega di inserirlo manualmente")
    else:
        with open('auth.txt', 'x'):
            pass

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

                requests_count += 1
                rate_limit.rate_minute()

                rate_limit_handler.wait_for_rate_limit_reset(response.headers['X-RateLimit-Remaining'],
                                                             response.headers['X-RateLimit-Reset'])
                # Gestisci la risposta
                if response.status_code == 200:
                    print("Richiesta riuscita!")
                    user = response.json()
                    print("Benvenut* :" + user['login'] +
                          '\n Questo è il nuovo tool di mining per GitHub. Le azioni consentite sono:'
                          '\n --a importIssue'
                          '\n --a importPullrequests'
                          '\n --a importWorkflowlogs'
                          '\n --a newAuth'
                          '\n --a filterOutput'
                          '\n --a search_repo'
                          '\n --a importPullrequestswithoutcomments'
                          '\n --a importIssuewithoutcomments'
                          '\n --a issuesWithParameters'
                          '\n --a pullReqWithParameters'
                          '\n --a esci ')
                    auth = True
                    with open('auth.txt', 'r+') as file:
                        line = file.readline()
                        line = args.AccessToken
                        file.seek(0)
                        file.writelines(line)

                else:
                    request_error_handler.request_error_handler(response.status_code)
                    print(
                        "Assicurati di aver inserito il token correttamente o che sia ancora valido per accedere all'API\n")
                    args.AccessToken = None

        if auth:

            if args.azione is None:
                args.azione = input("Inserisci l'azione che desideri effettuare: ")
            if args.azione == 'importIssue':
                issue_handler.save_github_issues(args.AccessToken, None, None)
                args.azione = None
            elif args.azione == 'importPullrequests':
                import_pull_requests.save_github_pull_requests(args.AccessToken)
                args.azione = None
            elif args.azione == 'importWorkflowlogs':
                import_and_save_workflow_logs.save_github_workflow_logs(args.AccessToken)
                args.azione = None
            elif args.azione == 'search_repo':
                search_repository.controller_repo(args.AccessToken)
                args.azione = None
            elif args.azione == 'importPullrequestswithoutcomments':
                import_pull_request_without_comments.save_github_pull_requests_without_comments(args.AccessToken)
                args.azione = None
            elif args.azione == 'importIssuewithoutcomments':
                import_issue_without_comments.save_github_issues_without_comments(args.AccessToken, None, None)
                args.azione = None
            elif args.azione == 'esci':
                print('Arrivederci!')
                break  # Esci dal loop
            elif args.azione == 'newAuth':
                args.azione = None
                args.AccessToken = None
                auth = False
            elif args.azione == 'filterOutput':
                filter_github()
                args.azione = None
            elif args.azione == 'issuesWithParameters':
                github_issues_with_par(args.AccessToken)
                args.azione = None
            elif args.azione == 'pullReqWithParameters':
                github_pullreq_with_par(args.AccessToken)
                args.azione = None
            else:
                print(f'Azione non riconosciuta. Le opzioni valide sono:'
                      '\n --a importIssue'
                      '\n --a importPullrequests'
                      '\n --a importWorkflowlogs'
                      '\n --a newAuth'
                      '\n --a filterOutput'
                      '\n --a search_repo'
                      '\n --a importPullrequestswithoutcomments'
                      '\n --a importIssuewithoutcomments'
                      '\n --a issuesWithParameters'
                      '\n --a pullReqWithParameters'
                      '\n --a esci ')
                args.azione = None


if __name__ == '__main__':
    main()
