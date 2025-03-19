import click
from githush.scan import scan_path

@click.group()
def main() -> None:
    pass

@click.command()
@click.argument("path", type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option("--staged-only", is_flag=True, help="Scan only staged files.")
@click.option(
    "--config-path",
    type=click.Path(exists=True),
    help="Path to the githush configuration file"
)
def scan(path: str, staged_only: bool, config_path: str) -> None:
    """Scan a repository or directory for exposed secrets."""
    results = scan_path(path, staged_only=staged_only, config_path=config_path)
    if results:
        click.echo("\nSecrets Found:")
        for file_path, secrets in results:
            click.echo(f"- {file_path}:")
            for line_number, secret in secrets:
                click.echo(f"    Line {line_number}: {secret[:50]}...")
    else:
        click.echo("No secrets found.")

main.add_command(scan)

if __name__ == "__main__":
    main()