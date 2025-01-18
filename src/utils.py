import os
import logging
import difflib
from typing import List, Set, Dict, Optional

import os
from pathlib import Path
from typing import List, Set, Tuple


def should_ignore_path(path: str, ignore_patterns: Set[str], shallow_ignore: Set[str]) -> Tuple[bool, bool]:
    """
    Check if path should be ignored and how.
    Returns (fully_ignore, shallow_ignore) tuple.
    """
    path_parts = Path(path).parts

    # Check for shallow ignore first
    if any(ignore == path_parts[0] for ignore in shallow_ignore):
        return False, True

    # Then check for full ignore
    return any(ignore in path_parts for ignore in ignore_patterns), False

def get_files_with_rglob(
    root_dir: str,
    max_depth: int = None,
    ignore_patterns: Set[str] = None,
    shallow_ignore: Set[str] = None,
    include_only: Set[str] = None,
) -> List[str]:
    """Get all files in a directory up to max_depth, handling different ignore patterns."""
    files = []
    root_path = Path(root_dir)
    
    for path in root_path.rglob("*"):
        if not path.is_file():
            continue
        
        relative_path = path.relative_to(root_path)
        
        # Check depth
        if max_depth is not None and len(relative_path.parts) > max_depth:
            continue
        
        # Check include_only patterns
        if include_only and not any(str(relative_path).startswith(pattern) for pattern in include_only):
            continue
            
        # Check ignore patterns
        fully_ignore, shallow_ignored = should_ignore_path(
            str(relative_path), ignore_patterns or set(), shallow_ignore or set()
        )
        
        if fully_ignore or shallow_ignored:
            continue
        
        files.append(str(relative_path))
    
    return sorted(files)

def get_files_with_oswalk(
    directory: str, 
    max_depth: Optional[int] = -1, 
    include_only: Set[str] = None, 
    ignore_patterns: Set[str] = None
) -> Dict[str, int]:
    """
    Traverse the directory and return files with their depth.
    
    Args:
        directory (str): The root directory to traverse.
        max_depth (Optional[int]): Maximum depth to traverse (-1 for no limit, None for no limit).
        include_only (Set[str]): Specific files/directories to include.
        ignore_patterns (Set[str]): Directories/files to ignore.
    
    Returns:
        Dict[str, int]: A dictionary with file paths as keys and their depth as values.
    """
    file_structure = {}
    root_depth = directory.rstrip(os.sep).count(os.sep)

    for root, dirs, files in os.walk(directory):
        current_depth = root.count(os.sep) - root_depth
        
        # Changed this line to handle None
        if max_depth is not None and max_depth != -1 and current_depth > max_depth:
            continue

        # Filter directories
        dirs[:] = [d for d in dirs if not should_ignore_name(d, ignore_patterns)]

        # Include specific directories only
        if include_only:
            dirs[:] = [d for d in dirs if d in include_only]

        for file in files:
            if include_only and not any(file.startswith(inc) for inc in include_only):
                continue
            if not should_ignore_name(file, ignore_patterns):
                file_structure[os.path.join(root, file)] = current_depth

    return file_structure


def should_ignore_name(name: str, patterns: Set[str] = None) -> bool:
    """
    Check if a file or directory matches any of the ignore patterns.
    Args:
        name (str): The name of the file or directory.
        patterns (Set[str]): Patterns to ignore.
    
    Returns:
        bool: True if the name should be ignored, False otherwise.
    """
    if not patterns:
        return False
    return any(pattern in name for pattern in patterns)

def get_directories_with_depth(
    root_dir: str,
    max_depth: int = None,
    ignore_patterns: Set[str] = None,
    shallow_ignore: Set[str] = None,
) -> List[str]:
    """Get all directories in a directory up to max_depth, handling ignore patterns."""
    dirs = set()
    root_path = Path(root_dir)

    for path in root_path.rglob("*"):
        if not path.is_dir():
            continue

        relative_path = path.relative_to(root_path)

        # Check depth
        if max_depth is not None and len(relative_path.parts) > max_depth:
            continue

        # Check ignore patterns
        fully_ignore, shallow_ignored = should_ignore_path(
            str(relative_path), ignore_patterns or set(), shallow_ignore or set()
        )

        if fully_ignore or shallow_ignored:  # Changed this condition to skip both fully ignored and shallow ignored
            continue

        dirs.add(str(relative_path))

    return sorted(list(dirs))

def compare_file_contents_full(file1: str, file2: str) -> bool:
    """Compare the contents of two files. Return True if they differ, False otherwise."""
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        return f1.read() != f2.read()

def compare_file_contents_diff(file1: str, file2: str) -> List[str]:
    """
    Compare the contents of two files and return the differences.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
    
    Returns:
        List[str]: List of differences, line by line.
    """
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        content1 = f1.readlines()
        content2 = f2.readlines()
        return list(difflib.unified_diff(content1, content2, lineterm=''))

def format_output(diff_results: Dict[str, List[str]]) -> str:
    """
    Format the differences for output in a human-readable way.

    Args:
        diff_results (Dict[str, List[str]]): A dictionary with file paths as keys and differences as values.
    
    Returns:
        str: A formatted string for output.
    """
    formatted = []
    for file_path, diff in diff_results.items():
        formatted.append(f"------- {file_path} -------")
        formatted.extend(diff)
        formatted.append("\n")
    return "\n".join(formatted)

def setup_logger(name: str, log_file: str = None, level: int = logging.INFO):
    """
    Set up a logger with optional file output.

    Args:
        name (str): Name of the logger.
        log_file (str): Optional file to save logs.
        level (int): Logging level.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

def write_to_file(output_file: str, content: str):
    """
    Write content to a file.

    Args:
        output_file (str): Path to the output file.
        content (str): Content to write.
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)

# Unified wrapper function to allow user to choose between rglob and os.walk methods
def get_files(
    root_dir: str,
    max_depth: int = None,
    ignore_patterns: Set[str] = None,
    shallow_ignore: Set[str] = None,
    method: str = "rglob",
) -> List[str]:
    if method == "rglob":
        return get_files_with_rglob(root_dir, max_depth, ignore_patterns, shallow_ignore)
    elif method == "os.walk":
        return get_files_with_oswalk(root_dir, max_depth, ignore_patterns)
    else:
        raise ValueError("Invalid method. Choose 'rglob' or 'os.walk'.")