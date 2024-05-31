import django.db.models.deletion
from django.db import migrations, models

import larek.apps.product.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog_category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Characteristic",
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
                        max_length=30, null=True, verbose_name="Characteristic"
                    ),
                ),
            ],
            options={
                "verbose_name": "Characteristic",
                "verbose_name_plural": "Characteristics",
                "db_table": "characteristic",
                "ordering": ["pk"],
            },
        ),
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
                        max_length=128, null=True, verbose_name="Product Name"
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
            name="ProductCharacteristic",
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
                    "description",
                    models.TextField(
                        max_length=300, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "characteristic",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="characteristic",
                        to="product.characteristic",
                        verbose_name="Characteristic",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_characteristic",
                        to="product.product",
                        verbose_name="Product",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Characteristic",
                "verbose_name_plural": "Product Characteristics",
                "db_table": "product_characteristic",
                "ordering": ["pk"],
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
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=128, verbose_name="Product Image Name"
                    ),
                ),
                (
                    "image",
                    models.FileField(
                        null=True,
                        upload_to=larek.apps.product.models.product_image_directory_path,
                        verbose_name="Product Image",
                    ),
                ),
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
