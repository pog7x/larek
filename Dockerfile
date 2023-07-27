FROM python:3.10.6

WORKDIR /app/

RUN pip install django psycopg2 uvicorn

COPY . .
