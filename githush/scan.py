import os
import re
import click
from typing import List
from git import Repo
from githush.config import load_config

SECRET_PATTERNS = [
    # Generic API keys, secrets, secret keys, and tokens
    r'(?i)(?:api[_-]?key|secret|secret[_-]?key|token)[\s:=]+["\']?[a-zA-Z0-9]{8,}["\']?',
    # Generic passwords
    r'(?i)(?:password|pwd|pw|passwd)[\s:=]+["\']?[^"\']{4,}["\']?',
    # GitHub tokens
    r'(?:ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}',
    # AWS Access Keys
    r'(?:AKIA|ASIA)[A-Z0-9]{16}',
    # Slack tokens
    r'xox[baprs]-[0-9A-Za-z]{10,48}',
    # Database connection strings
    r'(?:mongodb|postgres|mysql|redis|couchdb)://[^\s]+',
    # JWT
    r'ey[A-Za-z0-9-_]+?\.[A-Za-z0-9-_]+\.([A-Za-z0-9-_]+)?',
    # Generic 32-character secrets (e.g., Azure secrets)
    r'[0-9a-fA-F]{32}',
    # Stripe keys
    r'sk_live_[0-9a-zA-Z]{24}',
]

def get_staged_files(repo: Repo) -> list:
    """Get list of staged files from the repo."""
    staged_files = []
    for diff in repo.index.diff("HEAD"):
        if diff.a_blob:  # Ensures it's a file
            staged_files.append(diff.a_path)  # Relative path to the file
    return staged_files

def get_staged_file_content(repo: Repo, filepath: str) -> str:
    """Retrieve the content of a staged file."""
    blob = repo.index.get(filepath).blob  # Get the blob object for the file
    return blob.data_stream.read().decode("utf-8")  # Decode the bytes to string

def get_files(path: str) -> List[str]:
    """Retrieve a list of files to scan in the repository or directory."""
    files_to_scan = []
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            files_to_scan.append(filepath)
    return files_to_scan

def get_file_content(path: str) -> str:
    """Retrieve the content of a file from the working directory."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        click.echo(f"Error reading {path}: {e}")
        return ""

def scan_content(file_content: str, regex_patterns: list) -> list:
    """Scan file content for secrets based on provided regex patterns."""
    findings = []
    for pattern in regex_patterns:
        matches = re.findall(pattern, file_content)
        if matches:
            findings.extend(matches)
    return findings

def scan_path(path: str, staged_only: bool = False, config_path: str = None) -> List[str]:
    """Scan a repository or folder for secrets."""
    result = []
    click.echo("Loading configuration...")
    config = load_config(config_path)
    exclude_extensions = config.get("exclude_extensions", [])
    exclude_paths = config.get("exclude_paths", [])
    regex_patterns = SECRET_PATTERNS + config.get("custom_patterns", [])
    if staged_only:
        repo = Repo(path)
        files = get_staged_files(repo)
    else:
        files = get_files(path)
    click.echo(f"Scanning {path} for secrets...")
    for file in files:
        if (
            not any(file.endswith(ext) for ext in exclude_extensions) and
            not any(re.search(pattern, file) for pattern in exclude_paths)
        ):
            content = get_staged_file_content(repo, file) if staged_only else get_file_content(file)

            findings = []
            for line_number, line in enumerate(content.splitlines(), start=1):
                secrets = scan_content(line, regex_patterns)
                for secret in secrets:
                    findings.append((line_number, secret))

            if findings:
                result.append((file, findings))
    return result