from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum, unique
from discworld_cli.domain.models import Book, Character


@unique
class RepositoryResult(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class BookRepository(ABC):
    @abstractmethod
    def record(self, book: Book) -> RepositoryResult: ...


class CharacterRepository(ABC):
    @abstractmethod
    def record(self, character: Character) -> RepositoryResult: ...


class CharacterToBookMappingRepository(ABC):
    @abstractmethod
    def record(self, book: Book, character: Character) -> RepositoryResult: ...
