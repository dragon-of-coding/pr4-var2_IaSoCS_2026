
import io
import tempfile
import unittest

from contextlib import redirect_stdout
from pathlib import Path

from books import (
    add_book,
    create_book,
    load_books,
    main,
    save_books,
    search_by_author,
)


class BooksTests(unittest.TestCase):

    def setUp(self):
        self.books = [
            create_book("War and Peace", "Leo Tolstoy"),
            create_book("The Hobbit", "J. R. R. Tolkien"),
        ]

    def test_empty_title_is_rejected(self):
        with self.assertRaises(ValueError):
            create_book("", "Writer")

    def test_empty_author_is_rejected(self):
        with self.assertRaises(ValueError):
            create_book("Book", "   ")

    def test_title_and_author_are_trimmed(self):
        book = create_book("  Book ", " Writer  ")

        self.assertEqual(
            book,
            {"title": "Book", "author": "Writer"}
        )

    def test_create_book_preserves_data(self):
        book = create_book("Дюна", "Фрэнк Герберт")

        self.assertEqual(book["title"], "Дюна")
        self.assertEqual(book["author"], "Фрэнк Герберт")

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "missing.json"

            self.assertEqual(load_books(path), [])

    def test_save_and_load_books(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            save_books(self.books, path)

            self.assertEqual(load_books(path), self.books)

    def test_add_book_saves_it(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            add_book("Book", "Author", path)

            self.assertEqual(
                load_books(path),
                [create_book("Book", "Author")]
            )

    def test_add_book_appends(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            add_book("First", "Alice", path)
            add_book("Second", "Bob", path)

            self.assertEqual(len(load_books(path)), 2)

    def test_invalid_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            path.write_text(
                "{broken",
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_books(path)

    def test_non_list_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            path.write_text("{}", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_books(path)

    def test_invalid_record_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            path.write_text(
                '[{"title": 5, "author": "Bob"}]',
                encoding="utf-8"
            )

            with self.assertRaises(ValueError):
                load_books(path)

    def test_author_search_ignores_case(self):
        results = search_by_author(
            self.books,
            "lEo ToLsToY"
        )

        self.assertEqual(
            [book["title"] for book in results],
            ["War and Peace"]
        )

    def test_author_search_matches_part(self):
        results = search_by_author(
            self.books,
            "TOLS"
        )

        self.assertEqual(len(results), 1)

    def test_unknown_author_returns_empty_list(self):
        results = search_by_author(
            self.books,
            "Nobody"
        )

        self.assertEqual(results, [])

    def test_blank_search_is_rejected(self):
        with self.assertRaises(ValueError):
            search_by_author(self.books, "  ")

    def test_cli_help_returns_zero(self):
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as result:
                main(["--help"])

        self.assertEqual(result.exception.code, 0)

    def test_cli_search_uses_example(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "books.json"

            save_books(self.books, path)

            output = io.StringIO()

            with redirect_stdout(output):
                result = main([
                    "search",
                    "tolstoy",
                    "--file",
                    str(path)
                ])

            self.assertEqual(result, 0)
            self.assertIn(
                "War and Peace",
                output.getvalue()
            )


if __name__ == "__main__":
    unittest.main()
