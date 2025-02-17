import click
from githush.scan import scan_repository

@click.group()
def main():
    """Githush: A CLI tool to scan repositories for secrets."""
    pass

@main.command()
@click.argument("path", type=click.Path(exists=True))
def scan(path):
    """Scan a repository or directory for exposed secrets."""
    click.echo(f"Scanning {path} for secrets...")
    scan_repository(path)

if __name__ == "__main__":
    main()