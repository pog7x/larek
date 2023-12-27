from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Delivery",
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
                    "price",
                    models.FloatField(default=0, null=True, verbose_name="Price"),
                ),
                (
                    "order_sum",
                    models.FloatField(default=0, null=True, verbose_name="Order Sum"),
                ),
                ("verbose", models.TextField(null=True, verbose_name="Verbose")),
            ],
            options={
                "verbose_name": "Delivery",
                "verbose_name_plural": "Deliveries",
                "db_table": "delivery",
            },
        ),
    ]
