import click
import pathlib
import sys
from githush.scan import scan_path, install_pre_commit_hook

@click.group(add_help_option=False)
#@click.help_option('--help', '-h', help='Show the help message and exit.')
def main() -> None:
    """A tool to scan folders and repositories for secrets."""
    pass

@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--staged-only", is_flag=True, help="Scan only staged files.")
@click.option(
    "--config-path",
    type=click.Path(exists=True),
    help="Path to the githush configuration file."
)
def scan(path: str, staged_only: bool, config_path: str) -> None:
    """Scan a repository or directory for exposed secrets."""
    path = str(pathlib.Path(path).resolve())
    results = scan_path(path, staged_only=staged_only, config_path=config_path)
    if results:
        click.echo("\nSecrets Found:")
        for file_path, secrets in results:
            click.echo(f"- {file_path}:")
            for line_number, secret in secrets:
                click.echo(f"    Line {line_number}: {secret[:50]}{'...' if len(secret) > 50 else ''}")
        sys.exit(1)
    else:
        click.echo("No secrets found.")
        sys.exit(0)

@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
def install_hook(path: str) -> None:
    """Install pre commit hook to block commits containing secrets."""
    install_pre_commit_hook(path)

main.add_command(scan)
main.add_command(install_hook)

if __name__ == "__main__":
    main()