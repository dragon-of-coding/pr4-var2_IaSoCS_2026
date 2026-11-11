
import argparse
import json
from pathlib import Path


def create_book(title: str, author: str) -> dict[str, str]:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Название книги не может быть пустым")

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Автор книги не может быть пустым")

    return {
        "title": title.strip(),
        "author": author.strip()
    }


def load_books(file_path: str | Path) -> list[dict[str, str]]:
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Некорректный JSON-файл") from exc

    if not isinstance(data, list):
        raise ValueError("Ожидается JSON-массив книг")

    for book in data:
        if (
            not isinstance(book, dict)
            or not isinstance(book.get("title"), str)
            or not book["title"].strip()
            or not isinstance(book.get("author"), str)
            or not book["author"].strip()
        ):
            raise ValueError("Некорректная запись о книге")

    return data


def save_books(
    books: list[dict[str, str]],
    file_path: str | Path
) -> None:
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(books, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )


def add_book(
    title: str,
    author: str,
    file_path: str | Path
) -> dict[str, str]:
    books = load_books(file_path)
    book = create_book(title, author)

    books.append(book)
    save_books(books, file_path)

    return book


def search_by_author(
    books: list[dict[str, str]],
    query: str
) -> list[dict[str, str]]:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Поисковый запрос не может быть пустым")

    needle = query.strip()

    return [
        book
        for book in books
        if needle in book["author"]
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Каталог книг"
    )

    commands = parser.add_subparsers(
        dest="command",
        required=True
    )

    add = commands.add_parser(
        "add",
        help="Добавить книгу"
    )
    add.add_argument("title")
    add.add_argument("author")
    add.add_argument("--file", default="books.json")

    show = commands.add_parser(
        "list",
        help="Показать книги"
    )
    show.add_argument("--file", default="books.json")

    search = commands.add_parser(
        "search",
        help="Поиск книг по автору"
    )
    search.add_argument("author")
    search.add_argument("--file", default="books.json")

    args = parser.parse_args(argv)

    try:
        if args.command == "add":
            book = add_book(
                args.title,
                args.author,
                args.file
            )

            print(
                f"Добавлена книга: "
                f"{book['title']} — {book['author']}"
            )
            return 0

        books = load_books(args.file)

        if args.command == "search":
            books = search_by_author(books, args.author)

        if not books:
            print("Книги не найдены")

        for number, book in enumerate(books, 1):
            print(
                f"{number}. {book['title']} — "
                f"{book['author']}"
            )

    except ValueError as exc:
        parser.error(str(exc))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
