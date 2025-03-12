import yaml

DEFAULT_CONFIG = {
    "exclude_extensions": [".jpg", ".png", ".exe", ".bin", ".pdf"],
    "exclude_paths": ["node_modules/", "vendor/"],
    "custom_patterns": []
}

def load_config(config_path: str = "githush-config.yaml") -> dict:
    """Load the user config and merge it with defaults."""
    try:
        with open(config_path, "r") as config_file:
            user_config = yaml.safe_load(config_file)
            return {**DEFAULT_CONFIG, **user_config}
    except FileNotFoundError:
        # If config file doesn't exist, fall back to defaults
        return DEFAULT_CONFIG