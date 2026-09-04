FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
# RUN curl -sSL https://install.python-poetry.org | python3 -
# ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Копируем файлы зависимостей ДО остального кода (чтобы кэшировать слой)
COPY pyproject.toml poetry.lock README.md ./

# Устанавливаем Poetry, если его нет в базовом образе
RUN pip install --no-cache-dir poetry

# Отключаем виртуальные окружения через env-переменную (чище, чем poetry config)
ENV POETRY_VIRTUALENVS_CREATE=false

# Ставим только основные зависимости
# RUN poetry install --no-interaction --no-ansi --only main
RUN poetry install --no-interaction --no-ansi

# Создаем venv внутри образа и ставим зависимости (без dev дл production-образа)
# RUN poetry config virtualenvs.create false \
#     && poetry install --no-interaction --no-ansi --no-dev

# Копируем весь код
COPY . .

# Открываем порт дл Django
#EXPOSE 8000

# Настраиваем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Команда по умолчанию - переопределим в docker-compose дл разных сервисов
#CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

CMD ["poetry", "run", "gunicorn", "-c", "gunicorn.conf.py", "config.wsgi:application"]

# Пример запуска (Gunicorn уже установлен через poetry add gunicorn ранее)
#CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
