from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Cart",
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
                    "products_count",
                    models.IntegerField(
                        default=0, null=True, verbose_name="Products Count"
                    ),
                ),
            ],
            options={
                "verbose_name": "Cart",
                "verbose_name_plural": "Carts",
                "db_table": "cart",
            },
        ),
    ]
