import typer
from rich import print
from discworld_cli.container import get_catalog_service

app = typer.Typer()


@app.command()  # Typer will use the function docstring as the command help
def add(
    name: str = typer.Option(
        ...,
        "--name",
        help='The name of the book, e.g. "The Colour of Magic"',
    ),
    number: int = typer.Option(
        ...,
        "--number",
        help="Release ordering of the book, e.g. 1",
    ),
):
    """Add a new Book to the database

    Example:\n
    \n
    add --name 'Guards! Guards!' --number 8

    """
    svc = get_catalog_service()
    res = svc.add_book(name=name, number=number)
    print(f"[green]Book[/green] {name}#{number} -> {res.value}")
