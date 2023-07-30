from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("product_seller", "0001_initial"),
        ("cart", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="product_seller",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cart",
                to="product_seller.productseller",
                verbose_name="Product Seller",
            ),
        ),
    ]
