# Import external dependencies
import json, re, rich, typer
from fnmatch import translate as glob_to_regex
from pathlib import Path
from typing import Annotated, Literal

# Import internal functions
import bundlr.defaults as defaults
import bundlr.discover as discover
import bundlr.display as display
import bundlr.filter as filters
import bundlr.io as io

# _bundle_files: discover and filter files, and read contents
def _bundle_files(target_dir, output_dir, inc):
    # Print header
    display.printBundlrHeader(target_dir)
    base_name = target_dir.name
    root = target_dir.resolve()
    if inc:
        display.matchMessage(inc, ign_dirs=defaults.IGNORE_DIRS, ign_files=defaults.IGNORE_FILES)
    else:
        display.matchMessage(matching='*', ign_dirs=defaults.IGNORE_DIRS, ign_files=defaults.IGNORE_FILES)
    include_patterns = filters.compile_include_patterns(inc)
    files = discover.collect_files(root, include_patterns)
    tree = discover.build_tree(root)
    return root, tree, files, base_name

# Create a JSON-formatted file bundle
def bundle_json(target_dir, output_dir, inc):
    root, tree, files, base_name = _bundle_files(target_dir, output_dir, inc)
    out_file = f'{base_name}.json'
    result = io.output_json(root, tree, files, out_file)
    display.printBundlrFooter(result, out_file)

# Create a markdown-formatted file bundle
def bundle_markdown(target_dir, output_dir, inc):
    root, tree, files, base_name = _bundle_files(target_dir, output_dir, inc)
    out_file = f'{base_name}.md'
    result = io.output_markdown(root, tree, files, out_file)
    display.printBundlrFooter(result, out_file)    
