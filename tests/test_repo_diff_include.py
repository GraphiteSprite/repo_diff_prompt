import unittest
import os
import sys
import tempfile
from pathlib import Path

sys.path.append(os.path.abspath('./src'))

from repo_diff_includes import generate_comparison_report

class TestRepoDiffIncludes(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for each test
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.path.join(self.test_dir, "original")
        self.modified_dir = os.path.join(self.test_dir, "modified")
        self.output_file = os.path.join(self.test_dir, "report.txt")
        
        # Create directory structure
        os.makedirs(os.path.join(self.original_dir, "src"))
        os.makedirs(os.path.join(self.original_dir, "tests"))
        os.makedirs(os.path.join(self.modified_dir, "src"))
        os.makedirs(os.path.join(self.modified_dir, "tests"))
        os.makedirs(os.path.join(self.modified_dir, "new_dir"))

    def tearDown(self):
        # Clean up temporary directories
        import shutil
        shutil.rmtree(self.test_dir)

    def test_basic_comparison(self):
        # Create test files in original directory
        with open(os.path.join(self.original_dir, "src/main.py"), 'w') as f:
            f.write("def main():\n    print('Hello')\n")
        
        # Create modified files
        with open(os.path.join(self.modified_dir, "src/main.py"), 'w') as f:
            f.write("def main():\n    print('Hello World')\n")
        
        generate_comparison_report(
            original_dir=self.original_dir,
            modified_dir=self.modified_dir,
            output_file=self.output_file
        )
        
        # Updated assertions to match actual output format
        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("(MODIFIED)", content)  # Updated to match actual output
            self.assertIn("def main():", content)
            self.assertIn("-    print('Hello')", content)
            self.assertIn("+    print('Hello World')", content)

    def test_include_only_filter(self):
        # Create files in different directories - no need to recreate directories
        with open(os.path.join(self.original_dir, "src/main.py"), 'w') as f:
            f.write("original content")
        with open(os.path.join(self.original_dir, "tests/test.py"), 'w') as f:
            f.write("test content")
        
        # Create modified files
        with open(os.path.join(self.modified_dir, "src/main.py"), 'w') as f:
            f.write("modified content")
        
        generate_comparison_report(
            original_dir=self.original_dir,
            modified_dir=self.modified_dir,
            output_file=self.output_file,
            include_only={"src"}
        )
        
        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("/src/main.py", content)
            self.assertNotIn("/tests/test.py", content)

    def test_ignore_patterns(self):
        # Create files including some to be ignored
        with open(os.path.join(self.original_dir, "src/main.py"), 'w') as f:
            f.write("content")
        
        os.makedirs(os.path.join(self.original_dir, ".git"))
        with open(os.path.join(self.original_dir, ".git/config"), 'w') as f:
            f.write("git config")
        
        generate_comparison_report(
            original_dir=self.original_dir,
            modified_dir=self.modified_dir,
            output_file=self.output_file,
            ignore_patterns={".git"}
        )
        
        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("src/main.py", content)
            self.assertNotIn(".git/config", content)

    def test_max_depth(self):
        # Create nested directory structure
        os.makedirs(os.path.join(self.original_dir, "src/nested/deep"), exist_ok=True)
        with open(os.path.join(self.original_dir, "src/nested/deep/file.py"), 'w') as f:
            f.write("deep content")
        with open(os.path.join(self.original_dir, "src/surface.py"), 'w') as f:
            f.write("surface content")
        
        generate_comparison_report(
            original_dir=self.original_dir,
            modified_dir=self.modified_dir,
            output_file=self.output_file,
            max_depth=2
        )
        
        with open(self.output_file, 'r') as f:
            content = f.read()
            self.assertIn("src/surface.py", content)
            self.assertNotIn("src/nested/deep/file.py", content)

if __name__ == "__main__":
    unittest.main()