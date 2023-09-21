# larek

```bash
    python manage.py makemigrations user --no-header && python manage.py makemigrations --no-header

    python manage.py loaddata fixtures/sample
    python manage.py createsuperuser
    python manage.py dumpdata cart catalog_category delivery order payment product product_seller review role seller user views_history --format json --indent 4 --verbosity 1 -o fixtures/sample.json -e admin
    python clear_migrations.py
    autoflake --verbose --recursive --remove-all-unused-imports --remove-unused-variables --in-place --exclude venv,migrations .
    isort .
    black .
```
