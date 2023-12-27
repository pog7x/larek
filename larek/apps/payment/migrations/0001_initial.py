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
                    "card_number",
                    models.TextField(
                        blank=True, null=True, verbose_name="Payment Card Number"
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        blank=True,
                        choices=[
                            (1, "Init"),
                            (2, "Processing"),
                            (3, "Error"),
                            (4, "Paid"),
                        ],
                        default=1,
                        null=True,
                        verbose_name="Payment Status",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Payment Created At"
                    ),
                ),
                (
                    "paid_at",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Payment Paid At"
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="payment",
                        to="order.order",
                        verbose_name="Payment Order",
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
