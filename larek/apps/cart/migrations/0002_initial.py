from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("order", "0001_initial"),
        ("product", "0001_initial"),
        ("seller", "0001_initial"),
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="order",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cart",
                to="order.order",
                verbose_name="Order",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="product",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cart",
                to="product.product",
                verbose_name="Product",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="seller",
            field=models.ManyToManyField(
                default=None,
                related_name="cart",
                to="seller.seller",
                verbose_name="Seller",
            ),
        ),
    ]
