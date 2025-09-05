from __future__ import annotations
from discworld_cli.domain.models import Book, Character
from discworld_cli.domain.repositories import (
    BookRepository,
    CharacterRepository,
    CharacterToBookMappingRepository,
    RepositoryResult,
)


class CatalogService:
    def __init__(
        self,
        books: BookRepository,
        characters: CharacterRepository,
        mappings: CharacterToBookMappingRepository,
    ) -> None:
        self.books = books
        self.characters = characters
        self.mappings = mappings

    def add_book(self, name: str, number: int) -> RepositoryResult:
        return self.books.record(Book(name=name, number=number))

    def add_character(self, name: str) -> RepositoryResult:
        return self.characters.record(Character(name=name))

    def map_character(
        self, book_name: str, book_number: int, character_name: str
    ) -> RepositoryResult:
        return self.mappings.record(
            Book(name=book_name, number=book_number),
            Character(name=character_name),
        )
