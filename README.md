# sudoblark.patterns.repository-enterprise

A small Typer CLI that demonstrates the Repository pattern in Python and how to swap persistence backends (JSON files vs SQLite) via a simple feature flag.

## Table of Contents

1. [About The Project](#about-the-project)  
2. [Getting Started](#getting-started)  
3. [Usage](#usage)  
4. [Architecture](#architecture)  
5. [Configuration](#configuration)   
6. [License](#license)  
7. [Contact](#contact)  
8. [Appendix: Quick Local Run](#appendix-quick-local-run)

## About The Project

This repo is a minimal, runnable demonstration of the Repository pattern with a Typer-based CLI. It keeps the domain separate from infrastructure implementations. The CLI exercises the repositories through a small “Discworld catalog” example (books, characters, mappings).

It should be considered supplementary to the following [blog post](https://sudoblark.com/blog/database-interoperability-in-python-with-the-repository-enterprise-pattern) which attempts to describe the pattern in more detail.

### Features

- Clean Repository ports with JSON & SQLite implementations  
- Feature flag to switch backend at runtime (`PERSIST_BACKEND=sqlite|json`)  
- Typer CLI with `books` and `characters` subcommands  
- Thin application service layer so the CLI stays simple 
- Idempotent writes and atomic JSON writes; `UNIQUE` constraints in SQLite

### Built With

- **Language**: Python 3.10+  
- **CLI**: [Typer](https://typer.tiangolo.com/), [Rich](https://rich.readthedocs.io/)  
- **Packaging**: `pyproject.toml` (PEP 621)  
- **Persistence**: stdlib `sqlite3` and JSON
- **Quality of life**: [flake8](https://flake8.pycqa.org/en/latest/), [Black](https://pypi.org/project/black/)

## Getting Started

> These instructions assume macOS/Linux. Windows works with PowerShell equivalents.

### Prerequisites

- Python **3.10+**
- (Recommended) a virtual environment

```bash
python3 -m venv .venv
source ./.venv/bin/activate   # Windows: .\.venv\Scripts\activate
```

### Installation

Clone and install the project in editable mode:

```bash
git clone https://github.com/sudoblark/sudoblark.patterns.repository-enterprise
cd sudoblark.patterns.repository-enterprise
pip install -U pip setuptools
pip install poetry
poetry install
```

This exposes the CLI entrypoint: `discworld-cli`, which has a minimal amount of helper
text you can access via `discworld-cli --help`

## Usage

### Backend selection (feature flag)

Choose a backend with environment variables:

```bash
# SQLite (default)
export PERSIST_BACKEND=sqlite
export SQLITE_PATH=./app.db

# or JSON files
export PERSIST_BACKEND=json
export JSON_DIR=./data
```

### CLI examples

```bash
# Add a book
discworld-cli books add --name 'Guards! Guards!' --number 8

# Add a character
discworld-cli characters add --name 'Sam Vimes'

# Map character to book
discworld-cli characters map --book-name 'Guards! Guards!' --book-number 8 --character-name 'Sam Vimes'
```

Expected output:

```
Book Guards! Guards!#8 -> success
Character Sam Vimes -> success
Map Sam Vimes -> Guards! Guards!#8: success
```

## Architecture

### Folder structure

```
sudoblark.patterns.repository-enterprisemo/
├─ pyproject.toml
├─ README.md
├─ discworld_cli/                      # package root
│  ├─ application/
│  │  └─ services.py              # Orchestrates domain + repositories
│  ├─ cli/
│  │  ├─ app.py                   # Typer app & command wiring
│  │  ├─ books.py                 # books commands
│  │  └─ characters.py            # characters commands
│  ├─ config/
│  │  └─ settings.py              # env-backed settings (feature flags, paths)
│  ├─ domain/
│  │  ├─ models.py                # Book, Character, CharacterToBookMapping
│  │  └─ repositories.py          # RepositoryResult Enum and base abstracts: BookRepository, CharacterRepository, MappingRepository
│  ├─ infrastructure/
│  │  ├─ json/
│  │  │  └─ repositories.py       # JSONFile*Repository implementations
│  │  └─ sqlite/
│  │     └─ repositories.py       # SQLite*Repository implementations
│  │  ├─ factory.py               # builds repo bundle based on feature flag
│  └─ container.py                # simple dependency injection: exposes singletons for CLI
```

### Domain & repositories (ports)

- `discworld_cli/domain/models.py` holds plain dataclasses for `Book`, `Character`, and `CharacterToBookMapping`.  
- `discworld_cli/domain/repositories.py` defines ABCs (`BookRepository`, `CharacterRepository`, `CharacterToBookMappingRepository`) and a `RepositoryResult` enum.  
  Domain code depends only on these ports—never on concrete backends.

### Infrastructure backends (adapters)

- `discworld_cli/infrastructure/json/repositories.py` stores data as JSON lists with atomic writes and de-duplication.  
- `discworld_cli/infrastructure/sqlite/repositories.py` stores data in SQLite with `UNIQUE` constraints and `INSERT OR IGNORE`.

The CLI never touches backend details. It calls application services, which rely on repository ports.

## Configuration

Environment variables:

| Variable          | Default  | Description                                        |
|-------------------|----------|----------------------------------------------------|
| `PERSIST_BACKEND` | `sqlite` | Choose backend: `sqlite` or `json`                 |
| `SQLITE_PATH`     | `app.db` | SQLite database path                               |
| `JSON_DIR`        | `data`   | Directory holding `books.json`, `characters.json`, `mappings.json` |

Example:

```bash
export PERSIST_BACKEND=json
export JSON_DIR=./tmp/data
discworld-cli books add --name 'Small Gods' --number 13
```

## License

Distributed under the BSD-3 Clause license. See `LICENSE.txt` for details.

## Contact

Author: **Benjamin Clark** — <https://sudoblark.com> · <https://www.linkedin.com/in/benni/>

## Appendix: Quick Local Run

```bash
# 1) create & activate venv
python3 -m venv .venv && source .venv/bin/activate

# 2) install
python -m pip install -U pip
python -m pip install -e .

# 3) choose backend
export PERSIST_BACKEND=sqlite   # or: json
export SQLITE_PATH=./app.db
export JSON_DIR=./data

# 4) demo commands
discworld-cli books add --name 'Guards! Guards!' --number 8
discworld-cli characters add --name 'Sam Vimes'
discworld-cli characters map --book-name 'Guards! Guards!' --book-number 8 --character-name 'Sam Vimes'
```