import typer
from rich import print
from discworld_cli.container import get_catalog_service

app = typer.Typer()


@app.command("add")
def add(
    name: str = typer.Option(
        ...,
        "--name",
        help='The name of the Character, e.g. "Om" (technically a god, sort of, read the book)',
    )
):
    """Add a new Character to the database

    Example:\n
    \n
    add --name 'Om'
    """
    svc = get_catalog_service()
    res = svc.add_character(name=name)
    print(f"[green]Character[/green] {name} -> {res.value}")


@app.command("map")
def map(
    book_name: str = typer.Option(
        ...,
        "--book-name",
        help='The name of the Book in which the Character appears, e.g. "Small Gods"',
    ),
    book_number: int = typer.Option(
        ...,
        "--book-number",
        help="Release ordering of the book, e.g. 13",
    ),
    character_name: str = typer.Option(
        ...,
        "--character-name",
        help='The name of the Character which appears in the book, e.g. "Om"',
    ),
):
    """Map an existing Character to an existing Book in the database

    Example:\n
    \n
    map --book-name 'Small Gods' --book-number 13 --character-name 'Om'
    """
    svc = get_catalog_service()
    res = svc.map_character(book_name, book_number, character_name)
    print(
        f"[cyan]Map[/cyan] {character_name} -> {book_name}#{book_number}: {res.value}"
    )
