import argparse
import logging
import os
from src.repo_diff_general import run_general
from src.repo_diff_unified import run_unified
from src.repo_diff_includes import run_includes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_paths(original_dir, modified_dir):
    """Validate the input directory paths."""
    if not os.path.isdir(original_dir):
        raise FileNotFoundError(f"Original directory does not exist: {original_dir}")
    if not os.path.isdir(modified_dir):
        raise FileNotFoundError(f"Modified directory does not exist: {modified_dir}")

def main():
    parser = argparse.ArgumentParser(description="File comparison tool")
    parser.add_argument("--method", required=True, choices=["general", "unified", "includes"], help="Comparison method")
    parser.add_argument("original_dir", help="Path to the original directory")
    parser.add_argument("modified_dir", help="Path to the modified directory")
    parser.add_argument("output_file", help="Path to the output report file")
    parser.add_argument("--ignore", nargs="*", default=[], help="Ignore patterns")
    parser.add_argument("--shallow-ignore", nargs="*", default=[], help="Shallow ignore directories")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum directory depth to compare")
    parser.add_argument("--include", nargs="*", default=[], help="Include patterns (for includes method)")

    args = parser.parse_args()

    # Validate directories
    validate_paths(args.original_dir, args.modified_dir)

    # Dispatch to the appropriate method
    if args.method == "general":
        run_general(
            original_dir=args.original_dir,
            modified_dir=args.modified_dir,
            output_file=args.output_file,
            ignore_patterns=set(args.ignore),
            shallow_ignore=set(args.shallow_ignore),
            max_depth=args.max_depth,
        )
    elif args.method == "unified":
        run_unified(
            original_dir=args.original_dir,
            modified_dir=args.modified_dir,
            output_file=args.output_file,
            ignore_patterns=set(args.ignore),
            shallow_ignore=set(args.shallow_ignore),
            max_depth=args.max_depth,
        )
    elif args.method == "includes":
        run_includes(
            original_dir=args.original_dir,
            modified_dir=args.modified_dir,
            output_file=args.output_file,
            include_patterns=set(args.include),
            ignore_patterns=set(args.ignore),
            shallow_ignore=set(args.shallow_ignore),
            max_depth=args.max_depth,
        )

    # Log completion
    logger.info(f"Comparison report saved to: {args.output_file}")

if __name__ == "__main__":
    main()
