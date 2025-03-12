import os
import re
from typing import List
from git import Repo
from githush.config import load_config

SECRET_PATTERNS = [
    r'(?i)(api[_-]?key|secret|token)[\s:=]+["\'][a-z0-9]{20,}["\']', #generic key
    r'(password|pwd|passwd|api_key|secret)\s*=\s*["\'][^"\']+["\']' , #generic password
    r'(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36}', #GitHub
    r'(AKIA|ASIA)[A-Z0-9]{16,}', #AWS
    r'xox[baprs]-[0-9A-Za-z]{10,48}', #Slack
    r'(mongodb|postgres|mysql|redis|couchdb)://[^\s]+' #db connection strings
    r'ey[A-Za-z0-9-_]+?\.[A-Za-z0-9-_]+\.([A-Za-z0-9-_]+)?', #JWT
    r'[0-9a-fA-F]{32}', #Azure
    r'sk_live_[0-9a-zA-Z]{24}', #Stripe
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
        print(f"Error reading {path}: {e}")
        return ""

def scan_file(file_content: str, regex_patterns: list = SECRET_PATTERNS) -> list:
    """Scan file content for secrets based on provided regex patterns."""
    findings = []
    for pattern in regex_patterns:
        matches = re.findall(pattern, file_content)
        if matches:
            findings.extend(matches)
    return findings

def scan_path(path: str, staged_only: bool = False) -> List[str]:
    """Scan a repository or folder for secrets."""
    result = []
    config = load_config()
    exclude_extensions = config.get("exclude_extensions", [])
    exclude_paths = config.get("exclude_paths", [])
    if staged_only:
        repo = Repo(path)
        files = get_staged_files(repo)
    else:
        files = get_files(path)
    for file in files:
        if not any(file.endswith(ext) for ext in exclude_extensions) and not any(excl in file for excl in exclude_paths):
            content = get_staged_file_content(repo, file) if staged_only else get_file_content(file)
            findings = scan_file(content)
            result.extend(findings)
    return result