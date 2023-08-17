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
                    models.TextField(null=True, verbose_name="Description"),
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
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "db_table": "product",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                ("name", models.CharField(blank=True, max_length=128)),
                ("image", models.FileField(null=True, upload_to="product")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="product.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product image",
                "verbose_name_plural": "Product images",
                "db_table": "product_image",
                "ordering": ["pk"],
            },
        ),
    ]
