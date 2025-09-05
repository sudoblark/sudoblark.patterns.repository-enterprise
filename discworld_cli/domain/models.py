from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    name: str
    number: int


@dataclass(frozen=True)
class Character:
    name: str


@dataclass(frozen=True)
class CharacterToBookMapping:
    book: Book
    character: Character
