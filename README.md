
# Book Catalogue — CI/CD Practice

Практическая работа № 4.
Вариант № 2.

Простое консольное приложение для хранения
и поиска книг по автору.

## Технологии

- Python 3.11.10
- uv
- unittest
- GitHub Actions
- Docker

## Возможности

- Добавление книги
- Просмотр каталога
- Поиск по имени автора
- Поиск без учёта регистра
- Хранение данных в JSON

## Запуск

```bash
uv sync
uv run python app.py --help
```

Добавить книгу:

```bash
uv run python app.py add "Dune" "Frank Herbert"
```

Показать каталог:

```bash
uv run python app.py list
```

Поиск в демонстрационных данных:

```bash
uv run python app.py search "tolstoy" --file books.json.example
```

## Тестирование

```bash
uv run python -m unittest discover -s tests -v
```

## CI/CD

Workflow расположен в .github/workflows/ci.yml.

Он выполняет проверку исходного кода,
автоматическое тестирование, формирование
артефактов и учебное развёртывание.

Documentation branch validation test.