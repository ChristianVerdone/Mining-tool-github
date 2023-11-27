import concurrent.futures


# ...

def parallel_request_github_issues(token, owner, repository):
    issues_list = []
    i = 1

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:
            # Utilizza map per eseguire in parallelo le richieste alle API GitHub
            results = list(executor.map(lambda x: request_github_issues(token, owner, repository, x), [i]))
            i += 1

            for response in results:
                if response.status_code == 200:
                    issues = response.json()
                    if not issues:
                        return issues_list

                    for issue in issues:
                        if issue['comments'] > 0:
                            comments = import_issue_comments(token, owner, repository, issue)
                            if comments is None:
                                return None
                        else:
                            comments = 0

                        issue['comments_content'] = comments
                    issues_list.extend(issues)
                else:
                    request_error_handler.request_error_handler(response.status_code)
                    return None

    return issues_list


def parallel_save_github_issues(token):
    owner = input("Inserisci il nome dell'owner (utente su GitHub): ")
    repository = input("Inserisci il nome del repository su GitHub: ")

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    issues_folder = make_issues_directory(repository)
    file_path = os.path.join(issues_folder, f'issues_with_comments_{timestamp}.json')

    issues_list = parallel_request_github_issues(token, owner, repository)

    if issues_list is not None:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(issues_list, json_file, ensure_ascii=False, indent=4)
        print(f"Le informazioni delle issue sono state salvate con successo nel file '{file_path}'")

# ...
