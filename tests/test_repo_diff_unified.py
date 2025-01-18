import unittest
from unittest.mock import patch, mock_open, call
import os
import sys

sys.path.append(os.path.abspath('./src'))
sys.path.append(os.path.abspath('./tests'))

from repo_diff_unified import generate_comparison_report

class TestRepoDiffUnified(unittest.TestCase):

    @patch('builtins.open', new_callable=mock_open)
    @patch('repo_diff_unified.get_files_with_oswalk')
    def test_generate_comparison_report(self, mock_get_files, mock_open_file):
        # Mock different return values for original and modified directories
        mock_get_files.side_effect = [
            ['file1.py', 'file2.py'],  # original directory
            ['file2.py', 'file3.py']   # modified directory
        ]

        # Set up mock file contents
        mock_handle = mock_open_file.return_value
        mock_handle.readlines.side_effect = [
            ['original content 1\n'],  # file1.py original
            ['original content 2\n'],  # file2.py original
            ['modified content 2\n'],  # file2.py modified
            ['new content 3\n']        # file3.py new
        ]

        # Call the function under test
        generate_comparison_report(
            original_dir='original_dir',
            modified_dir='modified_dir',
            output_file='output_report.txt',
            ignore_patterns={'*.txt'},
            shallow_ignore={'dir_to_ignore'},
            max_depth=2
        )

        # Verify the calls to get_files_with_oswalk
        mock_get_files.assert_has_calls([
            call('original_dir', 2, {'*.txt'}, {'dir_to_ignore'}),
            call('modified_dir', 2, {'*.txt'}, {'dir_to_ignore'})
        ])

        # Instead of checking exact call sequence, verify specific write operations
        write_calls = mock_handle.write.call_args_list
        expected_writes = [
            call('\n------- file1.py (DELETED) -------\n'),
            call('\n------- file2.py (ORIGINAL) -------\n'),
            call('\n------- file2.py (CHANGES) -------\n'),
            call('\n------- file3.py (NEW) -------\n')
        ]
        
        # Check that all expected writes occurred
        for expected_call in expected_writes:
            self.assertIn(expected_call, write_calls)

        # Verify file opens occurred with correct paths
        open_calls = [
            call('output_report.txt', 'w', encoding='utf-8'),
            call('original_dir/file1.py', 'r', encoding='utf-8'),
            call('original_dir/file2.py', 'r', encoding='utf-8'),
            call('modified_dir/file2.py', 'r', encoding='utf-8'),
            call('modified_dir/file3.py', 'r', encoding='utf-8')
        ]
        
        # Verify that each expected open call exists in the actual calls
        for expected_call in open_calls:
            self.assertIn(expected_call, mock_open_file.call_args_list)

    @patch('builtins.open', new_callable=mock_open)
    @patch('repo_diff_unified.get_files_with_oswalk')
    def test_generate_comparison_report_with_changes(self, mock_get_files, mock_open_file):
        # Mock return values for both directories
        mock_get_files.side_effect = [
            ['file1.py'],  # original directory
            ['file1.py']   # modified directory
        ]

        # Mock different content for original and modified files
        mock_handle = mock_open_file.return_value
        mock_handle.readlines.side_effect = [
            ['print("Hello World")\n'],  # original content
            ['print("Goodbye World")\n']  # modified content
        ]

        # Run the comparison
        generate_comparison_report(
            original_dir='original_dir',
            modified_dir='modified_dir',
            output_file='output_report.txt'
        )

        # Verify specific write operations occurred
        write_calls = mock_handle.write.call_args_list
        
        # Check for headers
        self.assertTrue(any('file1.py (ORIGINAL)' in str(call) for call in write_calls))
        self.assertTrue(any('file1.py (CHANGES)' in str(call) for call in write_calls))

if __name__ == '__main__':
    unittest.main()