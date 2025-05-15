# Githush 

`Githush` is a CLI tool that scans repositories for exposed secrets and prevents unsafe commits using Git hooks and CI/CD pipelines.  


## Features  

- **Secret scanning** for exposed credentials in repositories  
- **Pre-commit hook integration** to block unsafe commits  
- **CI/CD compatibility** to enforce security in pipelines  


## Installation

**Note:** this package is not published on `PyPI`, in order to install `Githush` you need to clone the repository and install it into a virtual environment.

### Clone the repository

```sh
git clone https://github.com/nyradhr/githush.git
cd githush
```

### Virtual environment setup

#### Create the virtual environment


Install `uv`

```sh
pipx install uv
```

Create the venv

```sh
uv venv
```

#### Activate the virtual environment

On Unix/Linux:

```sh
source .venv/bin/activate 
```

On Windows:

```sh
.venv\Scripts\activate
```


## Usage

### Scan a repository
```
Usage: githush scan [OPTIONS] PATH

  Scan a repository or directory for exposed secrets.

Options:
  --staged-only       Scan only staged files.
  --config-path PATH  Path to the githush configuration file.
  --help              Show this message and exit.
```

### Install the pre-commit git hook

```
Usage: githush install-hook [OPTIONS] PATH

  Install pre commit hook to block commits containing secrets.

Options:
  --help  Show this message and exit.
```

## For contributing developers

The following command installs the dependencies from the optional groups in pyproject.toml

```sh
uv pip install .[dev, lint] 
```

Run tests

```sh
uv run pytest
```

Run linters

```sh
uv run ruff check .
```

Run type checking

```sh
mypy githush
```