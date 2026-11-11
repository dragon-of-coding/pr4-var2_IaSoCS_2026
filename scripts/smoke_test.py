
import os
import subprocess
import sys

from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit(
            "Usage: smoke_test.py <deploy-directory>"
        )

    dist = Path(sys.argv[1]).resolve()

    app = dist / "books.py"
    example = dist / "books.json.example"

    if not app.is_file() or not example.is_file():
        raise SystemExit("Missing deployment files")

    # Принудительно используем UTF-8 для дочерних процессов.
    child_env = os.environ.copy()
    child_env["PYTHONIOENCODING"] = "utf-8"

    # Проверка запуска справки --help.
    help_result = subprocess.run(
        [sys.executable, str(app), "--help"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=child_env
    )

    if (
        help_result.returncode != 0
        or "search" not in help_result.stdout
    ):
        raise SystemExit(
            f"Help smoke test failed: {help_result.stderr}"
        )

    # Проверка поиска автора в example-файле.
    search_result = subprocess.run(
        [
            sys.executable,
            str(app),
            "search",
            "tOlStOy",
            "--file",
            str(example)
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=child_env
    )

    if (
        search_result.returncode != 0
        or "War and Peace" not in search_result.stdout
        or "Anna Karenina" not in search_result.stdout
    ):
        raise SystemExit(
            f"Search smoke test failed: {search_result.stderr}"
        )

    # Формирование отчёта о развёртывании.
    report = (
        "Deployment smoke test: SUCCESS\n"
        "Environment: test/books\n"
        f"Commit: {os.environ.get('GITHUB_SHA', 'local')}\n"
        f"Run ID: {os.environ.get('GITHUB_RUN_ID', 'local')}\n"
        "--help: PASS\n"
        "Example author search: PASS\n"
    )

    Path("deployment.txt").write_text(
        report,
        encoding="utf-8"
    )

    print(report)


if __name__ == "__main__":
    main()
