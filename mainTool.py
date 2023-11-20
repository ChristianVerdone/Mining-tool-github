import argparse
import requests
import issue_handler
from function_filter import filter_github
import import_and_save_workflow_logs
import import_pull_requests
import request_error_handler
import time
import datetime
import json


def main():
    parser = argparse.ArgumentParser(description='Un esempio di tool a riga di comando.')

    parser.add_argument('AccessToken', nargs='?', default=None, help='Il token di accesso per API token')
    parser.add_argument('--azione', choices=['importIssue', 'importPullrequests', 'importWorkflowlogs'
                                             'esci', 'newAuth', 'filterOutput', 'mineAlltxt'], help='Azione da eseguire.')

    args = parser.parse_args()
    auth = False

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

        # Gestisci la risposta
        if response.status_code == 200:
            args.AccessToken = temp
            auth = True
            user = response.json()
            print("Benvenut* :" + user[
                'login'] + '\n Questo è il nuovo tool di mining per GitHub. Le azioni consentite sono:'
                           '\n --azione importIssue'
                           '\n --azione importPullrequests'
                           '\n --azione importWorkflowlogs'
                           '\n --azione newAuth'
                           '\n --azione filterOutput'
                           '\n --azione esci '
                           '\n --azione mineAlltxt')
        else:
            request_error_handler.request_error_handler(response.status_code)

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
                          '\n --azione mineAlltxt'
                          '\n --azione filterOutput')
                    auth = True
                    with open('auth.txt', 'r+') as file:
                        line = file.readline()
                        line = args.AccessToken
                        file.seek(0)
                        file.writelines(line)

                else:
                    request_error_handler.request_error_handler(response.status_code)
                    print("Assicurati di aver inserito il token correttamente o che sia ancora valido per accedere all'API\n")
                    args.AccessToken = None

        if auth:
            # Attendi il reset del limite di richieste API
            wait_for_rate_limit_reset(headers)  

            if args.azione is None:
                args.azione = input("Inserisci l'azione che desideri effettuare: ")

            if args.azione == 'importIssue':
                issue_handler.save_github_issues(args.AccessToken)
                args.azione = None
            elif args.azione == 'importPullrequests':
                import_pull_requests.save_github_pull_requests(args.AccessToken)
                args.azione = None
            elif args.azione == 'importWorkflowlogs':
                import_and_save_workflow_logs.save_github_workflow_logs(args.AccessToken)
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
            else:
                print(f'Azione non riconosciuta. Le opzioni valide sono: importIssue, importPullrequests, importWorkflowlogs, newAuth, filterOutput, esci')
                args.azione = None


def wait_for_rate_limit_reset(header):
    # Imposta l'URL per ottenere i dettagli del limite di richieste API dal servizio di GitHub.
    endpoint = "https://api.github.com/rate_limit"
    # Esegue una richiesta GET all'endpoint del limite di richieste API di GitHub utilizzando la libreria requests. 
    # Il parametro headers contiene l'autorizzazione necessaria per accedere all'API di GitHub.
    rate = requests.get(endpoint, headers=header)
    # Converte la risposta della richiesta in formato JSON per poter facilmente accedere ai dati contenuti.
    rateData = json.loads(rate.text)
    # Ottiene il timestamp Unix che indica quando il limite di richieste API sarà ripristinato. 
    # Il numero di richieste rimanenti per lo slot time attuale
    remaining = rateData['resources']['core']['remaining']
    print(f"remaining requests : {remaining}")
    if remaining == 0:
        # Questo valore rappresenta il tempo in cui il limite verrà resettato, consentendo nuovamente le richieste.
        resetTime = rateData['resources']['core']['reset']
        # Ottiene l'istante attuale.
        ms = datetime.datetime.now()
        # Ottiene il timestamp Unix corrente.
        nowTs = int(time.mktime(ms.timetuple()))
        # Calcola la differenza tra il tempo di reset del limite di richieste e il tempo corrente.
        diffTime = resetTime - nowTs
        # Verifica se diffTime è maggiore di zero, cioè se il tempo rimanente prima del reset del limite è positivo.
        if diffTime > 0:
            # Stampa un messaggio che avverte che il limite di richieste API è stato superato e indica il tempo rimanente prima del reset.
            print(f"Superato il limite di richieste API. Attendi {diffTime} secondi prima di continuare.")
            # Fa dormire il programma per diffTime secondi, quindi attende fino a quando
            # il limite di richieste API è stato resettato prima di continuare con le richieste successive.
            time.sleep(diffTime)


if __name__ == '__main__':
    main()
