from __future__ import annotations
from dataclasses import dataclass
import sqlite3
from os import PathLike
from discworld_cli.domain.repositories import (
    BookRepository,
    CharacterRepository,
    CharacterToBookMappingRepository,
    RepositoryResult,
)
from discworld_cli.domain.models import Book, Character

Pathish = str | PathLike[str]


SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS books (
  id     INTEGER PRIMARY KEY,
  name   TEXT NOT NULL,
  number INTEGER NOT NULL,
  UNIQUE(name, number)
);

CREATE TABLE IF NOT EXISTS characters (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS character_book_mappings (
  book_id      INTEGER NOT NULL,
  character_id INTEGER NOT NULL,
  PRIMARY KEY (book_id, character_id),
  FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
  FOREIGN KEY (character_id) REFERENCES characters(id) ON DELETE CASCADE
);
"""


class _SQLiteRepoBase:
    def __init__(self, db: Pathish | sqlite3.Connection):
        if isinstance(db, sqlite3.Connection):
            self.conn = db
            self._owns = False
        else:
            self.conn = sqlite3.connect(db)
            self._owns = True
        self.conn.row_factory = sqlite3.Row
        self.conn.executescript(SCHEMA_SQL)
        self.conn.commit()

    def close(self) -> None:
        if self._owns:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


# SQLite Book
@dataclass
class SQLiteBookRepository(_SQLiteRepoBase, BookRepository):
    db: Pathish | sqlite3.Connection

    def __post_init__(self):  # dataclass hook
        super().__init__(self.db)

    def record(self, book: "Book") -> RepositoryResult:
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO books(name, number) VALUES (?, ?)",
                (book.name, book.number),
            )
            self.conn.commit()
            return RepositoryResult.SUCCESS
        except sqlite3.Error:
            return RepositoryResult.FAILED


# SQLite Character
@dataclass
class SQLiteCharacterRepository(_SQLiteRepoBase, CharacterRepository):
    db: Pathish | sqlite3.Connection

    def __post_init__(self):
        super().__init__(self.db)

    def record(self, character: "Character") -> RepositoryResult:
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO characters(name) VALUES (?)",
                (character.name,),
            )
            self.conn.commit()
            return RepositoryResult.SUCCESS
        except sqlite3.Error:
            return RepositoryResult.FAILED


# SQLite Mapping
@dataclass
class SQLiteCharacterToBookMappingRepository(
    _SQLiteRepoBase, CharacterToBookMappingRepository
):
    db: Pathish | sqlite3.Connection

    def __post_init__(self):
        super().__init__(self.db)

    def record(self, book: "Book", character: "Character") -> RepositoryResult:
        try:
            self.conn.execute(
                "INSERT OR IGNORE INTO books(name, number) VALUES (?, ?)",
                (book.name, book.number),
            )
            self.conn.execute(
                "INSERT OR IGNORE INTO characters(name) VALUES (?)",
                (character.name,),
            )
            self.conn.execute(
                """
                INSERT OR IGNORE INTO character_book_mappings(book_id, character_id)
                VALUES (
                  (SELECT id FROM books WHERE name=? AND number=?),
                  (SELECT id FROM characters WHERE name=?)
                )
                """,
                (book.name, book.number, character.name),
            )
            self.conn.commit()
            return RepositoryResult.SUCCESS
        except sqlite3.Error:
            return RepositoryResult.FAILED
