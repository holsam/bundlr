'''
CLI entrypoints
'''

# Import external dependencies
import typer
from pathlib import Path
from typing import Annotated, Literal

# Import internal functions
from bundlr.main import bundle_json, bundle_markdown

# Instantiate Typer classes for each CLI command, each with:
#   Rich formatting
#   Disabled Typer completion hints
#   Help text shown if called without arguments
bundlr = typer.Typer(rich_markup_mode='rich', add_completion=False, no_args_is_help=True)
bundlrmd = typer.Typer(rich_markup_mode='rich', add_completion=False, no_args_is_help=True)
bundlrjs = typer.Typer(rich_markup_mode='rich', add_completion=False, no_args_is_help=True)

# Define shared typer argument/option signature
TargetDir = Annotated[
    Path,
    typer.Argument(help='Directory to bundle', show_default=False, dir_okay=True, file_okay=False, readable=True, exists=True),
]
OutputDir = Annotated[
    Path | None,
    typer.Option('-o', '--output', help='Output directory to save bundled file to'),
]
Incl = Annotated[
    list[str] | None,
    typer.Option('-i', '--include', help='Regex expression or glob pattern (e.g. *.ext)'),
]

# Define command functions for each CLI command
@bundlr.command()
def main(
    target_dir: TargetDir,
    output_dir: OutputDir = Path('.'),
    inc: Incl = None,
    fmt: Annotated[
        Literal['md', 'markdown', 'js', 'json'],
        typer.Option('-f', '--outfmt', help='Output format to use'),
    ] = 'md',
):
    if fmt in ['md', 'markdown']:
        bundle_markdown(target_dir, output_dir, inc)
    elif fmt in ['js', 'json']:
        bundle_json(target_dir, output_dir, inc)
    else:
        raise ValueError
    
@bundlrmd.command()
def main(
    target_dir: TargetDir,
    output_dir: OutputDir = Path('.'),
    inc: Incl = None,
):
    bundle_markdown(target_dir, output_dir, inc)

@bundlrjs.command()
def main(
    target_dir: TargetDir,
    output_dir: OutputDir = Path('.'),
    inc: Incl = None,
):
    bundle_json(target_dir, output_dir, inc)