import os
import sys
import difflib
from typing import List, Set, Tuple
from pathlib import Path
import argparse
from utils import get_files_with_rglob, should_ignore_path, get_directories_with_depth  # Imported new function

sys.path.append(os.path.abspath('./src'))
 

def generate_comparison_report(
    original_dir: str,
    modified_dir: str,
    output_file: str,
    ignore_patterns: Set[str] = None,
    shallow_ignore: Set[str] = None,
    max_depth: int = None
) -> None:
    """Generate a formatted comparison report between two directories."""
    
    # Get files and directories from both repos
    original_files = set(get_files_with_rglob(original_dir, max_depth, ignore_patterns, shallow_ignore))
    modified_files = set(get_files_with_rglob(modified_dir, max_depth, ignore_patterns, shallow_ignore))
    
    original_dirs = set(get_directories_with_depth(original_dir, max_depth, ignore_patterns, shallow_ignore))  # Updated to use the function from utils.py
    modified_dirs = set(get_directories_with_depth(modified_dir, max_depth, ignore_patterns, shallow_ignore))  # Same here
    
    all_files = sorted(original_files | modified_files)
    all_dirs = sorted(original_dirs | modified_dirs)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write directory structure
        f.write("/repository-root\n")
        
        # Track current directory for tree structure
        current_dirs = []
        
        # First write all directories
        for dir_path in all_dirs:
            parts = Path(dir_path).parts
            for i, dir_name in enumerate(parts):
                if i >= len(current_dirs):
                    prefix = "│   " * i
                    status = ""
                    if dir_name in shallow_ignore:
                        status = " [CONTENTS IGNORED]"
                    f.write(f"{prefix}├── {dir_name}/{status}\n")
                    current_dirs.append(dir_name)
                elif dir_name != current_dirs[i]:
                    current_dirs[i:] = [dir_name]
                    prefix = "│   " * i
                    status = ""
                    if dir_name in shallow_ignore:
                        status = " [CONTENTS IGNORED]"
                    f.write(f"{prefix}├── {dir_name}/{status}\n")
        
        # Then write all files
        for file_path in all_files:
            parts = Path(file_path).parts
            dirs = parts[:-1]
            
            # Write file entry with status
            prefix = "│   " * len(dirs)
            status = ""
            if file_path not in original_files:
                status = " [NEW]"
            elif file_path not in modified_files:
                status = " [DELETED]"
            else:
                # Compare file contents
                with open(os.path.join(original_dir, file_path), 'r', encoding='utf-8') as orig:
                    with open(os.path.join(modified_dir, file_path), 'r', encoding='utf-8') as mod:
                        if orig.read() != mod.read():
                            status = " [MODIFIED]"
            
            f.write(f"{prefix}└── {parts[-1]}{status}\n")
        
        # Write file contents
        f.write("\n")
        for file_path in all_files:
            if file_path in original_files and file_path in modified_files:
                # For modified files, show diff
                with open(os.path.join(original_dir, file_path), 'r', encoding='utf-8') as orig:
                    with open(os.path.join(modified_dir, file_path), 'r', encoding='utf-8') as mod:
                        original_content = orig.readlines()
                        modified_content = mod.readlines()
                        
                        if original_content != modified_content:
                            f.write(f"\n------- {file_path} (BEFORE) -------\n")
                            f.writelines(original_content)
                            f.write(f"\n------- {file_path} (AFTER) -------\n")
                            f.writelines(modified_content)
            
            elif file_path in modified_files:
                # For new files, show content
                with open(os.path.join(modified_dir, file_path), 'r', encoding='utf-8') as mod:
                    f.write(f"\n------- {file_path} (NEW) -------\n")
                    f.write(mod.read())
