from unittest.mock import patch

import mainTool


def test_mainTool_Path():
    with patch('os.path.exists') as mock_exists:
        mainTool.main()

    mock_exists.assert_called()

