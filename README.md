# Githush 

**Githush** is a CLI tool that scans repositories for exposed secrets and prevents unsafe commits using Git hooks and CI/CD pipelines.  

## Features  

- **Secret scanning** for exposed credentials in repositories  
- **Pre-commit hook integration** to block unsafe commits  
- **CI/CD compatibility** to enforce security in pipelines  

---

## Installation

### Clone the Repository

```sh
git clone https://github.com/nyradhr/githush.git
cd githush
```

### Using pip (for end users)

```sh
pip install .
```

### Using `uv` (for developers)

```sh
uv venv          # Create a virtual environment
source .venv/bin/activate  # Activate it (Linux/macOS)
.venv\Scripts\activate     # Activate it (Windows)

uv pip install .[dev, lint] #Installs all dependencies, including the optional groups
```

## Usage

### Scan a repository

Scans the given repository for hardcoded secrets.

```sh
githush scan path/to/repository
```

### Installing the pre-commit git hook

To prevent committing secrets, install the hook:

```sh
githush install-hook path/to/repository
```

## Development setup

### Run Tests

```sh
uv run pytest
```

### Run Linters

```sh
uv run ruff check .
```

### Run Type Checking

```sh
mypy githush
```