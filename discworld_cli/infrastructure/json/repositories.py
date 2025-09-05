from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import tempfile
import os
from os import PathLike
from discworld_cli.domain.repositories import (
    BookRepository,
    CharacterRepository,
    CharacterToBookMappingRepository,
    RepositoryResult,
)
from discworld_cli.domain.models import Book, Character

Pathish = str | PathLike[str]


def _read_list(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def _atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=path.parent, encoding="utf-8"
    ) as tmp:
        tmp.write(text)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def _write_list(path: Path, data: list[dict[str, Any]]) -> None:
    _atomic_write_text(path, json.dumps(data, indent=2, ensure_ascii=False))


# JSON Book
@dataclass
class JSONFileBookRepository(BookRepository):
    file_path: Pathish

    def record(self, book: "Book") -> RepositoryResult:
        path = Path(self.file_path)
        items = _read_list(path)
        exists = any(
            i.get("name") == book.name and i.get("number") == book.number for i in items
        )
        if not exists:
            items.append({"name": book.name, "number": book.number})
        _write_list(path, items)
        return RepositoryResult.SUCCESS


# JSON Character
@dataclass
class JSONFileCharacterRepository(CharacterRepository):
    file_path: Pathish

    def record(self, character: "Character") -> RepositoryResult:
        path = Path(self.file_path)
        items = _read_list(path)
        if not any(i.get("name") == character.name for i in items):
            items.append({"name": character.name})
        _write_list(path, items)
        return RepositoryResult.SUCCESS


# JSON Mapping
@dataclass
class JSONFileCharacterToBookMappingRepository(CharacterToBookMappingRepository):
    file_path: Pathish

    def record(self, book: Book, character: Character) -> RepositoryResult:
        path = Path(self.file_path)
        items = _read_list(path)
        entry = {
            "book": {"name": book.name, "number": book.number},
            "character": {"name": character.name},
        }
        exists = any(
            i.get("book", {}).get("name") == entry["book"]["name"]
            and i.get("book", {}).get("number") == entry["book"]["number"]
            and i.get("character", {}).get("name") == entry["character"]["name"]
            for i in items
        )
        if not exists:
            items.append(entry)
        _write_list(path, items)
        return RepositoryResult.SUCCESS
