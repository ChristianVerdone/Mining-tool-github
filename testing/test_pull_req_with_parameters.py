import pull_req_with_parameters


def test_exit(capsys, monkeypatch):
    inputs = iter(['esci',
                   'esci'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Token valido
    pull_req_with_parameters.github_pullreq_with_par('')
    captured = capsys.readouterr()

    assert 'Uscita dalla funzione.' in captured.out


def test_200_ok(capsys, monkeypatch):
    inputs = iter(['tensorflow',
                   'tensorflow',
                   'esci',
                   'esci'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    # Token valido
    pull_req_with_parameters.github_pullreq_with_par('')
    captured = capsys.readouterr()

    assert 'Uscita dalla funzione.' in captured.out
