'''
Input/output functions
'''

# Import external dependencies
import json
from pathlib import Path

# _make_markdown_header: returns string corresponding to markdown header
def _make_markdown_header(root: Path, tree: str) -> str:
    code_fence = '```'
    return (
        f'# Bundle: {root}\n\n'
        f'## Bundled Structure\n'
        f'{code_fence}\n{tree}\n{code_fence}\n\n'
        f'## File Content\n'
    )

# read_file_safe: returns string if path can be read as text otherwise raise an Exception
def read_file_safe(path: Path) -> str:
    try:
        return path.read_text(encoding='utf-8')
    except Exception:
        try:
            return path.read_text(encoding='latin-1')
        except Exception:
            return '[UNREADABLE FILE]'

# output_markdown: returns boolean: True if markdown file created successfully; False if not
def output_markdown(root, tree, files, output_base):
    try:
        with open(output_base, 'w', encoding='utf-8') as f:
            f.write(_make_markdown_header(root, tree))
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
        return True
    except Exception as e:
        print(e)
        return False
