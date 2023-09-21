from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "sum",
                    models.FloatField(default=0, null=True, verbose_name="Payment Sum"),
                ),
                (
                    "status",
                    models.TextField(max_length=30, null=True, verbose_name="Status"),
                ),
                (
                    "created_at",
                    models.DateTimeField(null=True, verbose_name="Payment Created At"),
                ),
                (
                    "order",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payment",
                        to="order.order",
                        verbose_name="Order",
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment",
                "verbose_name_plural": "Payments",
                "db_table": "payment",
            },
        ),
    ]
