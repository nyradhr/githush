# Githush

**Githush** is a CLI tool that scans repositories for exposed secrets and prevents unsafe commits using Git hooks and CI/CD pipelines.

---

## 🚀 Features

- 🔍 **Secret scanning** for exposed credentials in repositories  
- 🔐 **Pre-commit hook integration** to block unsafe commits  
- ⚙️ **CI/CD compatibility** to enforce security in pipelines

---

## 📦 Installation

Install via [pipx](https://pypa.github.io/pipx/), which safely installs CLI tools in isolated environments:

```sh
pipx install githush
```

Alternatively, install directly via pip:


```sh
pip install githush
```

## 🧪 Usage

### 🔍 Scan a repository
```
Usage: githush scan [OPTIONS] PATH

  Scan a repository or directory for exposed secrets.

Options:
  --staged-only       Scan only staged files.
  --config-path PATH  Path to the githush configuration file.
  --help              Show this message and exit.
```

### 🪝 Install the pre-commit git hook

```
Usage: githush install-hook [OPTIONS] PATH

  Install pre commit hook to block commits containing secrets.

Options:
  --help  Show this message and exit.
```

## 🧑‍💻 For contributing developers


### 🛠 Clone the repository

```sh
git clone https://github.com/nyradhr/githush.git
cd githush
```

### 🐍 Set up virtual environment with uv


1. Install `uv`

```sh
pipx install uv
```

2. Create the virtual environment:

```sh
uv venv
```

3. Activate the virtual environment

    - Unix/macOS:

    ```sh
    source .venv/bin/activate 
    ```

    - Windows:

    ```sh
    .venv\Scripts\activate
    ```

### 📥 Install dev dependencies

```sh
uv pip install .[dev, lint] 
```

### 🧪 Run tests

```sh
uv run pytest
```

### 🧹 Run linter

```sh
uv run ruff check .
```

### 🔎 Run static type checks

```sh
mypy githush
```