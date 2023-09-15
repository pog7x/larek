from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("delivery", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                    "city_to",
                    models.TextField(
                        max_length=30, null=True, verbose_name="Order City"
                    ),
                ),
                (
                    "address_to",
                    models.TextField(
                        max_length=30, null=True, verbose_name="Order Address"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(null=True, verbose_name="Order Created At"),
                ),
                (
                    "delivery",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order",
                        to="delivery.delivery",
                        verbose_name="Order Delivery",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="order",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Order User",
                    ),
                ),
            ],
            options={
                "verbose_name": "Order",
                "verbose_name_plural": "Orders",
                "db_table": "order",
            },
        ),
    ]
