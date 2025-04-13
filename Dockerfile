FROM python:3.12

ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Установите необходимые зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry

RUN poetry install --no-root

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
