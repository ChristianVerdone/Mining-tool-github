from unittest.mock import patch

import search_repository


def test_request_github_ratelimit():
    with patch('rate_limit_handler.wait_for_rate_limit_reset') as mocklimit:
        search_repository.request_github('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', 'jmpoep',
                                         'vmprotect-3.5.1')
    mocklimit.assert_called()
