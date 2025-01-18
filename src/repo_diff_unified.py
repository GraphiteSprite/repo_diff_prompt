import os
import sys
from typing import List, Set, Optional
import argparse
import difflib

# Adding src to the Python path so modules in src/ can be imported
sys.path.append(os.path.abspath('./src'))

# Importing the function from utils.py
from utils import get_files_with_oswalk


def generate_comparison_report(
    original_dir: str,
    modified_dir: str,
    output_file: str,
    ignore_patterns: Set[str] = None,
    shallow_ignore: Set[str] = None,
    max_depth: int = None
) -> None:
    """
    Generate a formatted comparison report between two directories.
    - Outputs original files with their content.
    - Displays only the differences in a unified diff format for modified files.
    - Includes the full content for new or deleted files.
    """
    try:
        original_files = set(get_files_with_oswalk(original_dir, max_depth, ignore_patterns, shallow_ignore))
        modified_files = set(get_files_with_oswalk(modified_dir, max_depth, ignore_patterns, shallow_ignore))

        all_files = sorted(original_files | modified_files)

        with open(output_file, 'w', encoding='utf-8') as f:
            for file_path in all_files:
                try:
                    if file_path in original_files and file_path in modified_files:
                        # Both versions exist, so compare them
                        with open(os.path.join(original_dir, file_path), 'r', encoding='utf-8') as orig:
                            with open(os.path.join(modified_dir, file_path), 'r', encoding='utf-8') as mod:
                                original_content = orig.readlines()
                                modified_content = mod.readlines()

                                if original_content != modified_content:
                                    f.write(f"\n------- {file_path} (ORIGINAL) -------\n")
                                    f.writelines(original_content)

                                    f.write(f"\n------- {file_path} (CHANGES) -------\n")
                                    diff = difflib.unified_diff(
                                        original_content,
                                        modified_content,
                                        fromfile="original",
                                        tofile="modified",
                                        lineterm=""
                                    )
                                    f.writelines(f"{line}\n" for line in diff)

                    elif file_path in modified_files:
                        # For new files, show the entire content
                        with open(os.path.join(modified_dir, file_path), 'r', encoding='utf-8') as mod:
                            f.write(f"\n------- {file_path} (NEW) -------\n")
                            f.writelines(mod.readlines())

                    elif file_path in original_files:
                        # For deleted files, show the original content
                        with open(os.path.join(original_dir, file_path), 'r', encoding='utf-8') as orig:
                            f.write(f"\n------- {file_path} (DELETED) -------\n")
                            f.writelines(orig.readlines())

                except (IOError, UnicodeDecodeError) as e:
                    f.write(f"\nError processing {file_path}: {str(e)}\n")
                    continue

    except Exception as e:
        raise RuntimeError(f"Failed to generate comparison report: {str(e)}")


def main():
    parser = argparse.ArgumentParser(description="Generate a comparison report between two directories.")
    parser.add_argument("original_dir", help="Path to the original directory.")
    parser.add_argument("modified_dir", help="Path to the modified directory.")
    parser.add_argument("output_file", help="Path to the output report file.")
    parser.add_argument("--ignore", nargs="*", default=[], help="List of file extensions or patterns to ignore.")
    parser.add_argument("--shallow-ignore", nargs="*", default=[], help="List of directories to shallow ignore.")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum directory depth to compare.")

    args = parser.parse_args()

    generate_comparison_report(
        original_dir=args.original_dir,
        modified_dir=args.modified_dir,
        output_file=args.output_file,
        ignore_patterns=set(args.ignore),
        shallow_ignore=set(args.shallow_ignore),
        max_depth=args.max_depth
    )


if __name__ == "__main__":
    main()