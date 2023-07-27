from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog_category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
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
                        max_length=30, null=True, verbose_name="Product Name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        max_length=999, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "catalog_category",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product",
                        to="catalog_category.catalogcategory",
                        verbose_name="Catalog Category",
                    ),
                ),
            ],
            options={
                "db_table": "product",
            },
        ),
    ]
