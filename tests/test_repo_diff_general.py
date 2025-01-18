import unittest
import os
import sys
import tempfile  # Add this import for the temporary directory

sys.path.append(os.path.abspath('./src'))
sys.path.append(os.path.abspath('./tests'))

from utils import get_files_with_rglob, get_directories_with_depth

class TestRepoDiff(unittest.TestCase):
    def test_include_filter(self):
    # First create a temporary test structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the directory structure
            src_dir = os.path.join(temp_dir, "src")
            dist_dir = os.path.join(temp_dir, "dist")
            os.makedirs(src_dir)
            os.makedirs(dist_dir)
            
            # Create test files
            with open(os.path.join(src_dir, "main.py"), 'w') as f:
                f.write("# test file")
            with open(os.path.join(dist_dir, "app.js"), 'w') as f:
                f.write("// test file")

            result = get_files_with_rglob(
                root_dir=temp_dir,
                include_only={"src", "tests"}
            )
        
        self.assertTrue("src/main.py" in result)
        self.assertFalse("dist/app.js" in result)
         
    
    def test_ignore_patterns(self):
        result = get_files_with_rglob(
            root_dir="sample_repo",  # Changed == to =
            ignore_patterns={".git", "node_modules"}
        )
        self.assertFalse(".git/config" in result)
        self.assertFalse("node_modules/library.js" in result)

    def test_get_directories_with_depth(self):
        # First create a temporary directory structure for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test directory structure
            os.makedirs(os.path.join(temp_dir, "src"))
            os.makedirs(os.path.join(temp_dir, "tests"))
            os.makedirs(os.path.join(temp_dir, "dist"))
            os.makedirs(os.path.join(temp_dir, ".git"))
            
            result = get_directories_with_depth(
                root_dir=temp_dir,
                max_depth=2,
                ignore_patterns={".git", "node_modules"},
                shallow_ignore={"dist"}
            )
            
            # Now test with relative paths
            self.assertTrue("src" in result)
            self.assertFalse("dist" in result)
            self.assertTrue("tests" in result)

if __name__ == "__main__":
    unittest.main()