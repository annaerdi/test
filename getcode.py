import os
from pathspec import PathSpec

GITIGNORE_PATTERNS = """
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
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST
*.manifest
*.spec
pip-log.txt
pip-delete-this-directory.txt
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/
cover/
*.mo
*.pot
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
instance/
.webassets-cache
.scrapy
docs/_build/
.pybuilder/
target/
.ipynb_checkpoints
profile_default/
ipython_config.py
.pdm.toml
.pdm-python
.pdm-build/
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
.idea/
.abstra/
.ruff_cache/
.pypirc
.cursorignore
.cursorindexingignore
logs/
uv.lock
.python-version
manual_tests/
/corecomponent_prototype.egg-info
/service_prototype.egg-info
code.drawio
output.txt
img.drawio
notes.md
test.ipynb
test 1.ipynb
output_1.txt
mkdocs.yml
client.py
server.py
manual.py
img.drawio
/tests
"""

def load_gitignore_patterns():
    """
    Create a PathSpec from embedded .gitignore patterns.

    Returns:
        PathSpec: A PathSpec object initialized with predefined patterns.
    """
    lines = GITIGNORE_PATTERNS.strip().splitlines()
    return PathSpec.from_lines('gitwildmatch', lines)


def write_files_to_txt(output_file='output', max_file_size_mb=5):
    """
    Write file paths and contents to text files, applying exclusions and size limits.

    Parameters:
        output_file (str): Base name for output files (default: 'output').
        max_file_size_mb (int): Maximum size of each output file in MB (default: 5).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    spec = load_gitignore_patterns()

    current_file_index = 1
    current_file_path = f"{output_file}_{current_file_index}.txt"
    current_file_size = 0

    outfile = open(current_file_path, 'w', encoding='utf-8')

    # Always start the first file with the header line
    header_text = "I have the following python project:\n\n"
    outfile.write(header_text)
    current_file_size += len(header_text)

    try:
        for root, dirs, files in os.walk(script_dir):
            # Exclude hidden directories and image folders
            dirs[:] = [d for d in dirs if not d.startswith('.') and d.lower() != 'images']

            for file in files:
                if file.startswith('.') or file == os.path.basename(__file__) or file.lower().endswith(('.png', '.gif')):
                    continue

                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, script_dir)

                # Skip files matching ignore patterns
                if spec.match_file(relative_path):
                    continue

                file_header = f"{relative_path}\n"
                if current_file_size + len(file_header) >= max_file_size_mb * 1024 * 1024:
                    outfile.close()
                    current_file_index += 1
                    current_file_path = f"{output_file}_{current_file_index}.txt"
                    outfile = open(current_file_path, 'w', encoding='utf-8')
                    current_file_size = 0

                outfile.write(file_header)
                current_file_size += len(file_header)

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        content = infile.read()
                        outfile.write(content)
                        current_file_size += len(content)
                except Exception as e:
                    error_message = f"Error reading file: {e}\n"
                    outfile.write(error_message)
                    current_file_size += len(error_message)

                separator = '\n' + '-' * 28 + '\n\n'
                outfile.write(separator)
                current_file_size += len(separator)
    finally:
        outfile.close()


if __name__ == '__main__':
    write_files_to_txt()
