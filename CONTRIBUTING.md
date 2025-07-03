# 🧑‍💻 Contributing to Githush

Thank you for your interest in contributing to **Githush**!  

---

## 📋 Prerequisites

Ensure you have the following installed:

- Python 3.12.3+
- [pipx](https://pypa.github.io/pipx/)
- [uv](https://github.com/astral-sh/uv) (package manager)

---

## 🛠 Getting Started

### Clone the Repository

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

## 🧼 Before Submitting a PR

Run all tests and linters

Ensure the README and docstrings are up to date

Follow existing naming conventions and style