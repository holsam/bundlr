'''
Filtering functions
'''

# Import external dependencies
import re
from pathlib import Path
from fnmatch import translate as glob_to_regex

# Import internal default constants
import bundlr.defaults as defaults

# is_binary: returns boolean: True if file extension is in BINARY_EXTENSIONS; False if not
def is_binary(file_path: Path) -> bool:
    return file_path.suffix.lower() in defaults.BINARY_EXTENSIONS

# should_ignore: returns boolean: True if path is in IGNORE_DIRS/FILES or file is binary
def should_ignore(path: Path) -> bool:
    parts = set(path.parts)
    if parts & defaults.IGNORE_DIRS:
        return True
    if path.name in defaults.IGNORE_FILES:
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