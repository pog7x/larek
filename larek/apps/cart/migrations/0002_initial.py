from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("cart", "0001_initial"),
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="order",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cart",
                to="order.order",
                verbose_name="Order",
            ),
        ),
    ]
