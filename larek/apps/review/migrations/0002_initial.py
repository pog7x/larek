from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("review", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="user",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="review",
                to=settings.AUTH_USER_MODEL,
                verbose_name="User",
            ),
        ),
    ]
