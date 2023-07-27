from django.db import models


class Role(models.Model):
    name = models.TextField(
        max_length=30,
        verbose_name="Role Name",
    )

    class Meta:
        db_table = "role"
