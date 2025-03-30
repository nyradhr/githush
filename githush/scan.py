import os
import re
import click
import stat
from typing import List
from pygit2 import Repository
from pygit2.enums import FileStatus
from githush.config import load_config

SECRET_PATTERNS = [
    # Generic API keys, secrets, secret keys, and tokens
    r'(?i)(?:api[_-]?key|key[_-]?id|secret|secret[_-]?key|client[_-]?secret|sig(?:nature)?|auth[_-]?key|access[_-]?token|refresh[_-]?token|token|keychain|bearer|my[_-]?secret[_-]?key)[\s:=]+["\']?[a-zA-Z0-9\-_]{4,}["\']?',
    # Generic passwords
    r'(?i)(?:password|pwd|pw|passwd|passcode|passphrase|cred(?:ential)?s?|login[_-]?secret|auth[_-]?password)[\s:=]+["\']?[^"\'\s]{4,}["\']?',
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

def get_files(path: str) -> List[str]:
    """Retrieve a list of files to scan in the repository or directory."""
    files_to_scan = []
    for root, _, files in os.walk(path):
        for file in files:
            filepath = os.path.join(root, file)
            files_to_scan.append(filepath)
    return files_to_scan

def get_file_content(file_path: str) -> str:
    """Retrieve the content of a file from the working directory."""
    try:
        with open(f"{file_path}", "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        click.echo(f"Error reading {file_path}: {e}")
        return ""

def scan_line(file_content: str, regex_patterns: list) -> list:
    """Scan a line of file content for secrets based on provided regex patterns."""
    findings = []
    for pattern in regex_patterns:
        matches = re.findall(pattern, file_content)
        if matches:
            findings.extend(matches)
    return findings

def scan_path(folder_path: str, staged_only: bool = False, config_path: str = "") -> list:
    """Scan a repository or folder for secrets."""
    result: list[tuple[str, list[tuple[int, str]]]] = []
    config = load_config(config_path)
    exclude_extensions = config.get("exclude_extensions", [])
    exclude_paths = config.get("exclude_paths", [])
    regex_patterns = SECRET_PATTERNS + config.get("custom_patterns", [])
    if staged_only:
        try:
            repo = Repository(folder_path)
            staged_files = []
            statuses = repo.status()

            for entry in repo.index:
                file_path = os.path.join(folder_path, entry.path)
                if (statuses.get(entry.path, 0) & FileStatus.INDEX_NEW or
                statuses.get(entry.path, 0) & FileStatus.INDEX_MODIFIED):
                    staged_files.append(file_path)

            files = staged_files
            if len(files) == 0:
                click.echo("No staged files to scan.")
                return result
        except Exception as e:
            click.echo(f"Error accessing Git repository at {folder_path}: {e}")
            return result
    else:
        files = get_files(folder_path)
    click.echo(f"Scanning {folder_path} for secrets...")
    for file in files:
        if (
            not any(file.endswith(ext) for ext in exclude_extensions) and
            not any(re.search(pattern, file) for pattern in exclude_paths)
        ):
            content = get_file_content(file)
            findings: list[tuple[int, str]] = []
            for line_number, line in enumerate(content.splitlines(), start=1):
                secrets = scan_line(line, regex_patterns)
                for secret in secrets:
                    findings.append((line_number, secret))

            if findings:
                result.append((file, findings))
    return result

def install_pre_commit_hook(repo_path: str) -> None:
    """Install a pre-commit hook in the specified repository."""
    if not os.path.exists(repo_path+"/.git"):
        click.echo("The given path does not correspond to a valid Git repository.")
    git_hooks_dir = os.path.join(repo_path, ".git", "hooks")
    pre_commit_hook_path = os.path.join(git_hooks_dir, "pre-commit")
    
    hook_script = """#!/bin/sh
githush scan $PWD --staged-only
if [ $? -ne 0 ]; then
    echo "Commit blocked due to detected secrets. Please fix them and try again."
    exit 1
fi
"""
    os.makedirs(git_hooks_dir, exist_ok=True)

    with open(pre_commit_hook_path, "w") as hook_file:
        hook_file.write(hook_script)

    st = os.stat(pre_commit_hook_path)
    os.chmod(pre_commit_hook_path, st.st_mode | stat.S_IEXEC)

    click.echo(f"Pre-commit hook installed successfully at {pre_commit_hook_path}!")