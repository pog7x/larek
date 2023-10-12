from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("seller", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductSeller",
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
                    "products_count",
                    models.IntegerField(
                        default=0, null=True, verbose_name="Products Count"
                    ),
                ),
                (
                    "price",
                    models.FloatField(default=0, null=True, verbose_name="Price"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_seller",
                        to="product.product",
                        verbose_name="Product",
                    ),
                ),
                (
                    "seller",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="product_seller",
                        to="seller.seller",
                        verbose_name="Seller",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product Seller",
                "verbose_name_plural": "Product Seller",
                "db_table": "product_seller",
            },
        ),
    ]
