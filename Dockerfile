FROM python:3.10.6

# WORKDIR /app/

# ENV PIP_DEFAULT_TIMEOUT=100 \
#     PIP_DISABLE_PIP_VERSION_CHECK=1 \
#     PIP_NO_CACHE_DIR=1 \
#     POETRY_VERSION=1.5.1 \
#     PYTHONUNBUFFERED=1

RUN pip install django psycopg2

# COPY pyproject.toml poetry.lock ./

# RUN poetry config virtualenvs.create false
# RUN poetry install --no-root --no-interaction --ansi

COPY . .