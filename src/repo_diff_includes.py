import os
import sys
from typing import List, Set, Optional
import argparse
import difflib
from utils import get_files_with_oswalk, should_ignore_path  # Changed to use consistent functions

sys.path.append(os.path.abspath('./src'))

def generate_comparison_report(
    original_dir: str,
    modified_dir: str,
    output_file: str,
    ignore_patterns: Set[str] = None,
    shallow_ignore: Set[str] = None,
    include_only: Set[str] = None,
    max_depth: int = None
) -> None:
    # Using get_files_with_oswalk for more concise output
    original_files = get_files_with_oswalk(
        directory=original_dir, 
        max_depth=max_depth, 
        include_only=include_only, 
        ignore_patterns=ignore_patterns
    )
    modified_files = get_files_with_oswalk(
        directory=modified_dir, 
        max_depth=max_depth, 
        include_only=include_only, 
        ignore_patterns=ignore_patterns
    )

    # Convert full paths to relative paths for comparison
    original_file_paths = {os.path.relpath(path, original_dir): depth 
                          for path, depth in original_files.items()}
    modified_file_paths = {os.path.relpath(path, modified_dir): depth 
                          for path, depth in modified_files.items()}

    # Combine the lists of file paths for both directories
    all_files = sorted(set(original_file_paths.keys()) | set(modified_file_paths.keys()))

    with open(output_file, 'w', encoding='utf-8') as f:
        for file_path in all_files:
            orig_full_path = os.path.join(original_dir, file_path)
            mod_full_path = os.path.join(modified_dir, file_path)
            
            if file_path in original_file_paths and file_path in modified_file_paths:
                # Both versions exist, so compare them
                with open(orig_full_path, 'r', encoding='utf-8') as orig:
                    with open(mod_full_path, 'r', encoding='utf-8') as mod:
                        original_content = orig.readlines()
                        modified_content = mod.readlines()

                        if original_content != modified_content:
                            f.write(f"\n------- {file_path} (MODIFIED) -------\n")
                            diff = difflib.unified_diff(
                                original_content,
                                modified_content,
                                fromfile="original",
                                tofile="modified",
                                lineterm=""
                            )
                            f.writelines(f"{line}\n" for line in diff)

            elif file_path in modified_file_paths:
                # For new files, show the content
                with open(mod_full_path, 'r', encoding='utf-8') as mod:
                    f.write(f"\n------- {file_path} (NEW) -------\n")
                    f.writelines(mod.readlines())

            elif file_path in original_file_paths:
                # For deleted files, show the content
                with open(orig_full_path, 'r', encoding='utf-8') as orig:
                    f.write(f"\n------- {file_path} (DELETED) -------\n")
                    f.writelines(orig.readlines())

