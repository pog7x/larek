from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Seller",
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
                    "name",
                    models.TextField(
                        max_length=30, null=True, verbose_name="Seller Name"
                    ),
                ),
                (
                    "phone",
                    models.TextField(
                        max_length=30, null=True, verbose_name="Seller Phone"
                    ),
                ),
                (
                    "address",
                    models.TextField(
                        max_length=100, null=True, verbose_name="Seller Address"
                    ),
                ),
                (
                    "email",
                    models.TextField(
                        max_length=30, null=True, verbose_name="Seller Email"
                    ),
                ),
            ],
            options={
                "db_table": "seller",
            },
        ),
    ]
