import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("product_seller", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Banner",
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
                    "type",
                    models.IntegerField(
                        choices=[
                            (1, "Main Slider"),
                            (2, "Limited Offers"),
                            (3, "Popular Goods"),
                            (4, "Limited Edition"),
                        ],
                        null=True,
                        verbose_name="Banner Type",
                    ),
                ),
                (
                    "expired_at",
                    models.DateTimeField(
                        null=True, verbose_name="Banner Product Expired At"
                    ),
                ),
                (
                    "product_seller",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="banner",
                        to="product_seller.productseller",
                        verbose_name="Product Seller",
                    ),
                ),
            ],
            options={
                "verbose_name": "Banner",
                "verbose_name_plural": "Banners",
                "db_table": "banner",
            },
        ),
    ]
