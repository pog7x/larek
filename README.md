# LAREK

## Make migrations

```bash
python manage.py makemigrations user --no-header && python manage.py makemigrations --no-header
```

## Clear migrations script

```bash
python clear_migrations.py
```

## Load fixtures

```bash
docker-compose exec app python manage.py loaddata fixtures/sample
```

## Dump DB data to fixtures

```bash
python manage.py dumpdata banner cart catalog_category delivery order payment product product_seller review seller user views_history --format json --indent 4 --verbosity 1 -o fixtures/sample.json -e admin
```
