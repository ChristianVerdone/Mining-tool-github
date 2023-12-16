from unittest.mock import patch

import mainTool


def test_importIssue(monkeypatch):
    inputs = iter(['importIssue',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('issue_handler.save_github_issues') as mock_issue:
        mainTool.main()

    mock_issue.assert_called()


def test_importPullrequests(monkeypatch):
    inputs = iter(['importPullrequests',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('import_pull_requests.save_github_pull_requests') as mock_Pullrequests:
        mainTool.main()

    mock_Pullrequests.assert_called()


def test_importWorkflowlogs(monkeypatch):
    inputs = iter(['importWorkflowlogs',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('import_and_save_workflow_logs.save_github_workflow_logs') as mock_Workflowlogs:
        mainTool.main()

    mock_Workflowlogs.assert_called()


def test_search_repo(monkeypatch):
    inputs = iter(['search_repo',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('search_repository.controller_repo') as mock_search_repo:
        mainTool.main()

    mock_search_repo.assert_called()


def test_importPullrequestswithoutcomments(monkeypatch):
    inputs = iter(['importPullrequestswithoutcomments',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch(
            'import_pull_request_without_comments.save_github_pull_requests_without_comments') as mock_Pullrequestswithoutcomments:
        mainTool.main()

    mock_Pullrequestswithoutcomments.assert_called()


def test_importIssuewithoutcomments(monkeypatch):
    inputs = iter(['importIssuewithoutcomments',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('import_issue_without_comments.save_github_issues_without_comments') as mock_Issuewithoutcomments:
        mainTool.main()

    mock_Issuewithoutcomments.assert_called()


def test_newAuth_filterOutput(monkeypatch):
    inputs = iter(['newAuth',
                   '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',  # inserire token valido
                   'filterOutput',
                   'repository',
                   'issues',
                   'esc',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('function_filter.filter_github') as mock_filterExit:
        mainTool.main()

    mock_filterExit.assert_not_called()


def test_newAuthNotValid(monkeypatch):
    inputs = iter(['newAuth',
                   '',  # token non valido
                   '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',  # token valido
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('request_error_handler.request_error_handler') as mock_notToken:
        mainTool.main()

    mock_notToken.assert_called()


def test_functionFilter(monkeypatch):
    inputs = iter(['filterOutput',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('function_filter.filter_github') as mock_filter:
        mainTool.main()

    mock_filter.assert_not_called()


def test_issuesWithParameters(monkeypatch):
    inputs = iter(['issuesWithParameters',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('issues_with_parameters.github_issues_with_par') as mock_issuesWithParameters:
        mainTool.main()

    mock_issuesWithParameters.assert_not_called()


def test_pullReqWithParameters(monkeypatch):
    inputs = iter(['pullReqWithParameters',
                   '',
                   '',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))

    with patch('pull_req_with_parameters.github_pullreq_with_par') as mock_pullReqWithParameters:
        mainTool.main()

    mock_pullReqWithParameters.assert_not_called()


def test_noAction(monkeypatch, capsys):
    inputs = iter(['',
                   'esci'])

    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    mainTool.main()
    # Cattura l'output per verifica
    captured = capsys.readouterr()

    # Verifica che l'output includa 'Arrivederci!'
    assert 'Arrivederci!' in captured.out



