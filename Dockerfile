FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./
RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry install --no-root --no-interaction

COPY . .

# Создаем директории для статики и медиа
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]