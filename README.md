# README.md
# repo-diff-prompt

A Python tool for generating human-readable comparisons between two versions of a repository, with support for selective directory traversal and intelligent ignore patterns. The tool was created to assist with context sharing with AI/LLM chat prompts by using the output to describe a repo where the chat prompt does not have access to the repo itself. 

Ideal Use Cases
When you need a comprehensive and visually detailed report of directory and file differences.
For analyzing changes in a structured repository, especially when directory context is important.

## Features
This repository contains three tools for comparing and analyzing differences between two directories. Each script has unique features and is tailored for specific use cases. Below is a summary of their functionality, ideal use cases, and usage examples.

- Directory tree visualization: Outputs a tree structure of the directory,      including shallow-ignored directories marked as [CONTENTS IGNORED].

- Detailed file comparison: Shows the full content of modified files in BEFORE and AFTER sections.

- File classification: Separates files into NEW, MODIFIED, and DELETED categories.
Custom ignore patterns:
-- Full ignore: Excludes files or directories completely.
-- Shallow ignore: Includes directories but excludes their contents.

- Support for specifically including files to be compared
- Configurable maximum directory depth
- UTF-8 support
- Clear, formatted output suitable for documentation or review

## Installation

```bash
# Clone the repository
git clone https://github.com/GraphiteSprite/repo-diff-prompt.git
cd repo-diff-prompt

# Optional: Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

- should_ignore_path
Use when you need to handle paths and check for both full and shallow ignores.
Example usage: File/directory traversal where shallow ignore is needed for top-level directories.
- should_ignore_name
Use for a simpler check when you only care about matching a name to ignore patterns.
Example usage: Quick filtering of individual file or directory names.

Basic comparison between two directories:
```bash
python repo_diff_prompt.py original_repo/ modified_repo/ output/output.txt
```

Advanced usage with inclusion patterns, ignore patterns, and depth control:
```bash
python repo_diff_includes.py original_repo/ modified_repo/ output/output.txt \
    --include src tests \
    --ignore node_modules .git \
    --shallow-ignore dist build \
    --max-depth 3

```

### Command Line Arguments

- `original_dir`: Path to the original repository directory
- `modified_dir`: Path to the modified repository directory
- `output_file`: Path where the comparison report will be saved
- `--ignore`: Patterns to completely ignore (including the directory itself)
- `--shallow-ignore`: Top-level directories to show but ignore contents
- `--max-depth`: Maximum directory depth to traverse

### Example Output

```
/repository-root
├── src/
│   ├── components/
│   │   └── Button.js [MODIFIED]
│   └── utils/
│       └── helpers.js
├── dist/ [CONTENTS IGNORED]
├── build/ [CONTENTS IGNORED]
└── package.json

------- src/components/Button.js (BEFORE) -------
import React from 'react';
const Button = ({ text }) => {
  return <button>{text}</button>;
};
export default Button;

------- src/components/Button.js (AFTER) -------
import React from 'react';
const Button = ({ text, onClick, variant = 'primary' }) => {
  return (
    <button onClick={onClick} className={`btn-${variant}`}>
      {text}
    </button>
  );
};
export default Button;
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# requirements.txt
pathlib>=1.0.1

---

# LICENSE
MIT License

Copyright (c) 2025 Graphite Sprite

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

# .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Operating System
.DS_Store
Thumbs.db