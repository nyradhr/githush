import yaml
import click

DEFAULT_CONFIG = {
    "exclude_extensions": [".jpg", ".png", ".exe", ".bin", ".pdf"],
    "exclude_paths": ["node_modules/", "vendor/", "\\."],
    "custom_patterns": []
}

def load_config(config_path: str = "githush-config.yaml") -> dict:
    """Load the user config and merge it with defaults."""
    if config_path is None:
        config_path = "githush-config.yaml"
    click.echo(f"Using config file: {config_path}")
    try:
        with open(config_path, "r") as config_file:
            user_config = yaml.safe_load(config_file)
            return {**DEFAULT_CONFIG, **user_config}
    except FileNotFoundError:
        click.echo(f"Configuration file '{config_path}' not found. Using defaults.")
        return DEFAULT_CONFIG