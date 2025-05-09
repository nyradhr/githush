import yaml
import click

DEFAULT_CONFIG = {
    "exclude_extensions": [".jpg", ".png", ".exe", ".bin", ".pdf", ".lock"],
    "exclude_paths": [r"(?:^|\/|\\)(?:node_modules|vendor|githush|tests)(\/|\\)", r"(?:^|[\\/])\.[^\\/]+(?:[\\/][^\\/]+)*"],
    "custom_patterns": []
}

def load_config(config_path: str) -> dict:
    """Load the user defined configuration settings; if there are none, uses the default configuration."""
    if config_path:
        try:
            with open(config_path, "r") as config_file:
                user_config = yaml.safe_load(config_file)
                click.echo(f"Using config file: {config_path}")
                return {**user_config}
        except FileNotFoundError:
            click.echo(f"Configuration file '{config_path}' not found. Using defaults.")
            return DEFAULT_CONFIG
        
    return DEFAULT_CONFIG # no config file