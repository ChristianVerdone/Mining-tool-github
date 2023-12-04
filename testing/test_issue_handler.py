import unittest
from unittest.mock import patch, MagicMock

# Importa il modulo contenente le funzioni da testare
import issue_handler  # Assicurati di sostituire "nome_del_tuo_modulo" con il nome effettivo del tuo modulo


class TestGitHubIssues(unittest.TestCase):

    @patch('builtins.input', side_effect=['owner', 'repository'])
    @patch('requests.get')
    @patch('json.dump')
    @patch('os.makedirs')
    @patch('os.path.exists', side_effect=[False, False])
    @patch('os.path.join', side_effect=['repository_data/issues',
                                        'repository_data/issues/issues_with_comments_2023-12-01_12-00-00.json'])
    def test_save_github_issues(self, mock_os_join, mock_os_path_exists, mock_os_makedirs, mock_json_dump,
                                mock_requests_get, mock_input):
        # Simula una risposta di successo dal server GitHub
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'number': 1, 'title': 'Issue 1', 'state': 'open', 'comments': 1}]
        mock_requests_get.return_value = mock_response

        # Simula la risposta del server GitHub per il conteggio dei commenti
        mock_comments_response = MagicMock()
        mock_comments_response.status_code = 200
        mock_comments_response.json.return_value = [{'user': {'login': 'user1'}, 'body': 'Commento 1'}]

        # Configura il comportamento del mock per la richiesta di commenti
        mock_requests_get.side_effect = [mock_response, mock_comments_response, mock_response]

        # Simula il reset del limite di richieste
        mock_reset_time = '123456789'
        mock_response.headers = {'X-RateLimit-Remaining': '4999', 'X-RateLimit-Reset': mock_reset_time}

        # Simula l'input dell'utente
        mock_input.return_value = 'owner', 'repository'

        # Simula la creazione della directory
        mock_os_path_exists.return_value = False

        # Simula il timestamp corrente
        mock_datetime_now = MagicMock()
        mock_datetime_now.strftime.return_value = '2023-12-01_12-00-00'
        with patch('datetime.datetime.now', mock_datetime_now):
            # Esegui la funzione da testare
            issue_handler.save_github_issues('token')

        # Verifica che le funzioni siano state chiamate correttamente
        mock_os_path_exists.assert_called_with('repository_data')
        mock_os_makedirs.assert_called_with('repository_data')
        mock_json_dump.assert_called_once()
        mock_requests_get.assert_called()
        mock_input.assert_called()
        mock_os_join.assert_called()

    # Aggiungi altri test se necessario


if __name__ == '__main__':
    unittest.main()
