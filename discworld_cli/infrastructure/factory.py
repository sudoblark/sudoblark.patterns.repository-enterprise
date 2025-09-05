from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal

from discworld_cli.domain.repositories import (
    BookRepository,
    CharacterRepository,
    CharacterToBookMappingRepository,
)
from discworld_cli.infrastructure.json.repositories import (
    JSONFileBookRepository,
    JSONFileCharacterRepository,
    JSONFileCharacterToBookMappingRepository,
)
from discworld_cli.infrastructure.sqlite.repositories import (
    SQLiteBookRepository,
    SQLiteCharacterRepository,
    SQLiteCharacterToBookMappingRepository,
)

Backend = Literal["sqlite", "json"]


@dataclass
class Repositories:
    books: BookRepository
    characters: CharacterRepository
    mappings: CharacterToBookMappingRepository
    close: Callable[[], None]


def make_repositories(
    *,
    backend: Backend,
    sqlite_path: str | Path = "app.db",
    json_dir: str | Path = "data",
) -> Repositories:
    if backend == "sqlite":
        conn = sqlite3.connect(sqlite_path)
        return Repositories(
            books=SQLiteBookRepository(db=conn),
            characters=SQLiteCharacterRepository(db=conn),
            mappings=SQLiteCharacterToBookMappingRepository(db=conn),
            close=conn.close,
        )
    elif backend == "json":
        base = Path(json_dir)
        return Repositories(
            books=JSONFileBookRepository(file_path=base / "books.json"),
            characters=JSONFileCharacterRepository(file_path=base / "characters.json"),
            mappings=JSONFileCharacterToBookMappingRepository(
                file_path=base / "mappings.json"
            ),
            close=lambda: None,
        )
    else:
        raise ValueError(f"Unknown backend: {backend!r}")
