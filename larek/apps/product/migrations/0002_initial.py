from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product", "0001_initial"),
        ("product_seller", "0001_initial"),
        ("seller", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sellers",
            field=models.ManyToManyField(
                through="product_seller.ProductSeller",
                to="seller.seller",
                verbose_name="Sellers",
            ),
        ),
    ]
