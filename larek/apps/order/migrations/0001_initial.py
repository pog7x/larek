from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("delivery", "0001_initial"),
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
                    "full_name",
                    models.TextField(
                        max_length=150, null=True, verbose_name="Order Full Name"
                    ),
                ),
                (
                    "phone",
                    models.TextField(blank=True, null=True, verbose_name="Order Phone"),
                ),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
                (
                    "address",
                    models.TextField(
                        max_length=300, null=True, verbose_name="Order Address"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Order Created At"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        blank=True,
                        choices=[(1, "Created"), (2, "Payment error"), (3, "Paid")],
                        default=1,
                        null=True,
                    ),
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
