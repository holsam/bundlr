'''
File discovery functions
'''
# Import external dependencies
from pathlib import Path

# Import internal functions
import bundlr.display as display
import bundlr.filter as filters

# build_tree: returns string of directory structure
def build_tree(root: Path) -> str:
    lines = []
    def _walk(current: Path, prefix=''):
        entries = sorted([p for p in current.iterdir() if not filters.should_ignore(p)])
        for i, entry in enumerate(entries):
            connector = '└── ' if i == len(entries) - 1 else '├── '
            if entry.is_file():
                lines.append(f'{prefix}{connector}{entry.name}')
            if entry.is_dir():
                lines.append(f'{prefix}{connector}{entry.name}/')
                extension = '    ' if i == len(entries) - 1 else '│   '
                _walk(entry, prefix + extension)
    _walk(root)
    return '\n'.join(lines)

# collect_files: returns list of paths
def collect_files(root: Path, include_patterns):
    all_contents = sorted(root.rglob('*'))
    search_files = [entry for entry in all_contents if entry.is_file()]
    display.printMessage(total=len(search_files))
    files = []
    for path in search_files:
        if not filters.should_ignore(path):
            if filters.matches_include(path, include_patterns):
                files.append(path)
    display.printMessage(matches=len(files))
    return files
