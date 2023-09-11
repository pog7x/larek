from django.db import migrations, models
import larek.apps.catalog_category.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CatalogCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.TextField(
                        max_length=30, verbose_name="Catalog Category Name"
                    ),
                ),
                (
                    "icon",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=larek.apps.catalog_category.models.catalog_category_icon_directory_path,
                        verbose_name="Catalog Category Icon",
                    ),
                ),
            ],
            options={
                "verbose_name": "Catalog Category",
                "verbose_name_plural": "Catalog Categories",
                "db_table": "catalog_category",
            },
        ),
    ]
