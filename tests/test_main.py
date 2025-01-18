from main import main
from unittest.mock import patch
import pytest
import os
import sys

sys.path.append(os.path.abspath('./src'))
sys.path.append(os.path.abspath('./tests'))

@patch("src.repo_diff_general.run_general")
def test_main_dispatch_general(mock_run_general):
    with patch("sys.argv", ["main.py", "--method", "general", "orig_dir", "mod_dir", "output.txt"]):
        main()
    mock_run_general.assert_called_once_with(
        "orig_dir", "mod_dir", "output.txt", set(), set(), None
    )
