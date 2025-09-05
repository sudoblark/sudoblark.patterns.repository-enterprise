import typer
from discworld_cli.cli import books, characters

app = typer.Typer(no_args_is_help=True)
app.add_typer(books.app, name="books", help="Book operations")
app.add_typer(characters.app, name="characters", help="Character operations")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
