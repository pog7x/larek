# LAREK

## Database scheme

![database scheme](docs/db_scheme.png 'Database scheme')

## Make migrations

```bash
python manage.py makemigrations user --no-header && python manage.py makemigrations --no-header
```

## Format code

```bash
chmod +x scripts/format.sh && ./scripts/format.sh
```

## Clear migrations script

```bash
python clear_migrations.py
```

## Load fixtures

```bash
python manage.py loaddata fixtures/sample
```

```bash
docker-compose exec app python manage.py loaddata fixtures/sample
```

## Dump DB data to fixtures

```bash
python manage.py dumpdata banner cart catalog_category delivery order payment product product_seller review role seller user views_history --format json --indent 4 --verbosity 1 -o fixtures/sample.json -e admin
```
