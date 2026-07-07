FROM python:3.10-slim

# Зависимости дл сборки
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Копируем алы зависимосте
COPY pyproject.toml poetry.lock ./

# Создаем venv внутри образа и ставим зависимости (без dev дл production-образа)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

# Копируем весь код
COPY . .

# Открываем порт дл Django
EXPOSE 8000

# Команда по умолчанию - переопределим в docker-compose дл разных сервисов
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
