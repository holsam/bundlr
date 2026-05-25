# Import external dependencies
import json, re, rich, typer
from fnmatch import translate as glob_to_regex
from pathlib import Path
from typing import Annotated, Literal

# Import internal functions
import bundlr.display as display

# Define directories to ignore during bundling
IGNORE_DIRS = {'.git', 'node_modules', 'dist', 'build', '__pycache__', '.venv', 'venv'}
# Define files to ignore during bundling
IGNORE_FILES = {'.DS_Store'}
# Define extensions of binary files
BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.pdf', '.zip', '.tar', '.gz', '.mp4', '.mp3', '.woff', '.woff2', '.ttf', '.eot'}

# Instantiate Typer class for bundlr
bundlr = typer.Typer(
    # Set markup mode so can use rich formatting
    rich_markup_mode='rich',
    # Disable the Typer add completion hints to help page
    add_completion=False,
    # Set that running comms command only provides help page
    no_args_is_help=True,
)

# is_binary: returns boolean: True if file extension is in BINARY_EXTENSIONS; False if not
def is_binary(file_path: Path) -> bool:
    return file_path.suffix.lower() in BINARY_EXTENSIONS

# should_ignore: returns boolean: True if path is in IGNORE_DIRS/FILES or file is binary
def should_ignore(path: Path) -> bool:
    parts = set(path.parts)
    if parts & IGNORE_DIRS:
        return True
    if path.name in IGNORE_FILES:
        return True
    if is_binary(path):
        return True
    return False

# compile_include_patterns: returns None or a list of strings (corresponding to regex patterns converted from globs) 
def compile_include_patterns(patterns):
    if not patterns:
        return None
    compiled = []
    for p in patterns:
        compiled.append(re.compile(glob_to_regex(p)))
    return compiled

# matches_include: returns boolean: True is files matching patterns are found; False if not
def matches_include(path: Path, patterns) -> bool:
    if patterns is None:
        return True
    path_str = str(path)
    return any(p.match(path_str) for p in patterns)
    
# build_tree: returns string of directory structure
def build_tree(root: Path) -> str:
    lines = []
    def _walk(current: Path, prefix=''):
        entries = sorted([p for p in current.iterdir() if not should_ignore(p)])
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
        if not should_ignore(path):
            if matches_include(path, include_patterns):
                files.append(path)
    display.printMessage(matches=len(files))
    return files

# read_file_safe: returns string if path can be read as text otherwise raise an Exception
def read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        try:
            return path.read_text(encoding='latin-1')
        except Exception:
            return '[UNREADABLE FILE]'

# make_markdown_header: returns string corresponding to markdown header
def make_markdown_header(root: Path, tree: str) -> str:
    code_fence = '```'
    return (
        f'# Bundle: {root}\n\n'
        f'## Bundled Structure\n'
        f'{code_fence}\n{tree}\n{code_fence}\n\n'
        f'## File Content\n'
    )

# output_markdown: returns boolean: True if markdown file created successfully; False if not
def output_markdown(root, tree, files, output_base):
    try:
        with open(output_base, 'w', encoding='utf-8') as f:
            f.write(make_markdown_header(root, tree))
            for file_path in files:
                rel_path = file_path.relative_to(root)
                content = read_file_safe(file_path)
                f.write(f'### FILE: {rel_path}\n{content}\n')
        return True
    except Exception as e:
        display.printError(e)
        return False

# output_json: returns boolean: True if JSON outputted successfully; False if not
def output_json(root, tree, files, output_base):
    try:
        data = {
            'structure': tree,
            'files': []
        }
        for file_path in files:
            rel_path = str(file_path.relative_to(root))
            content = read_file_safe(file_path)
            data['files'].append({
                'path': rel_path,
                'content': content
            })
        with open(output_base, 'w', encoding='utf-8') as out:
            json.dump(data, out, indent=2)
    except Exception as e:
        print(e)
        return False





# main: bundlr command logic
@bundlr.command()
def main(
    target_dir: Annotated[
        Path,
        typer.Argument(help='Directory to bundle', show_default=False, dir_okay=True, file_okay=False, readable=True, exists=True),
    ],
    output_dir: Annotated[
        Path | None,
        typer.Option('-o', '-outdir', help='Output directory to save bundled file to'),
    ] = Path('.'),
    fmt: Annotated[
        Literal['md', 'markdown', 'json'],
        typer.Option('-f', '--outfmt', help='Output format to use'),
    ] = 'md',
    inc: Annotated[
        list[str] | None,
        typer.Option('-i', '--include', help='Regex expression or glob pattern (e.g. *.ext)'),
    ] = None,
):
    # Convert format to file extension
    if fmt in ['md','markdown']:
        fmt = 'md'
    # Print header
    display.printBundlrHeader(target_dir)
    base_name = target_dir.name
    root = target_dir.resolve()
    if inc:
        display.matchMessage(inc, ign_dirs=IGNORE_DIRS, ign_files=IGNORE_FILES)
    else:
        display.matchMessage(matching='*', ign_dirs=IGNORE_DIRS, ign_files=IGNORE_FILES)
    include_patterns = compile_include_patterns(inc)
    files = collect_files(root, include_patterns)
    tree = build_tree(root)
    if fmt == 'md':
        result = output_markdown(root, tree, files, f'{base_name}.md')
    else:
        result = output_json(root, tree, files, f'{base_name}.json')
    if result:
        display.printSuccessFooter(target_dir, output_dir, fmt)
    else:
        display.printFailureFooter()