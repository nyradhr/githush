import click
from githush.scan import scan_path

@click.group()
def main() -> None:
    pass

@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--staged-only", is_flag=True, help="Scan only staged files.")
def scan(path: str, staged_only: bool) -> None:
    """Scan a repository or directory for exposed secrets."""
    click.echo(f"Scanning {path} for secrets...")
    scan_path(path, staged_only)

main.add_command(scan)

if __name__ == "__main__":
    main()