FROM python:3.11.10-slim

WORKDIR /app

COPY books.py app.py books.json.example ./

CMD ["python", "app.py", "--help"]