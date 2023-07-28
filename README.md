# larek

```bash
python manage.py makemigrations --no-header
python clear_migrations.py
autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place --exclude venv,migrations .
isort .
black .
```