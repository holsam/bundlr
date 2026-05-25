'''
src/bundlr/display.py

Functions for displaying bundlr terminal output
'''
# Import external dependencies
import os
from pathlib import Path
from rich import print

# Define constants
bundlr_title = '🧵 bundlr'

# _printDivider: helper function to create a divider line, with optional embedded text
def _printDivider(
        char: str = "=",
        embed: str | None = None
    ):
    terminal_width = os.get_terminal_size().columns - 1
    if not embed:
        print(f'{char * terminal_width}')
    else:
        embed_length = len(embed) + 2
        half_width = (terminal_width-embed_length)//2
        if ((2 * half_width) + embed_length) == terminal_width:
            header_text = f'{char*half_width} {str(embed)} {char*half_width}'
            print(header_text)
        else:
            header_text = f'{char*half_width} {str(embed)} {char*(half_width+1)}'
            print(header_text)


def _formatDirFiles(dirs, files):
    out = []
    for item in sorted(dirs):
        out_item = str(item)+'/'
        out.append(out_item)
    for item in sorted(files):
        out.append(item)
    return ", ".join(out)

# printBundlrHeader: prints header/start splash to terminal
def printBundlrHeader(target_dir: Path):
    print(f'\n')
    _printDivider(char='=', embed=bundlr_title)
    print(f'[bold]Bundling target directory:[/bold] [cyan]{target_dir.resolve()}[/cyan]')

# printSuccessFooter: prints footer for succeeded bundle to terminal
def printSuccessFooter(target_dir: Path, output_dir: Path, fmt: str):
    print(f'[bold]Output bundle file wrote to:[/bold] [cyan]{output_dir}/{target_dir.name}.{fmt}[/cyan]')
    _printDivider(char='=', embed=bundlr_title)
    print(f'\n')

# printFailureFooter: prints footer for failed bundle to terminal
def printFailureFooter(target_dir: Path, output_dir: Path, fmt: str):
    print(f'[red][bold]Output bundle file could not be created[/bold][/red]')
    _printDivider(char='=', embed=bundlr_title)
    print(f'\n')

# matchMessage: prints message about matching 
def matchMessage(matching, ign_dirs, ign_files):
    print(
        f'[bold]File matching patterns:[/bold]\n'
        f'\t[green][bold]✓[/bold] {",".join(matching)}[/green]\n'
        f'\t[red][bold]✗[/bold] {_formatDirFiles(ign_dirs, ign_files)}[/red]'
    )    

# printMessage: prints generic messages
def printMessage(total: int | None = None, matches: int | None = None):
    if total:
        print(f'[bold]Total files found:[/bold] [white]{str(total)}[/white]')
    if matches:
        print(f'[bold]Matching files found:[/bold] [white]{str(matches)}[/white]')

# printError: prints errors
def printError(errorMsg):
    print(f'\t[yellow][bold]WARNING:[/bold] could not process files: {errorMsg}[/yellow]')