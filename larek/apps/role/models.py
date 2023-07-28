from django.db import models


class Role(models.Model):
    name = models.TextField(
        max_length=30,
        verbose_name="Role Name",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "role"
        verbose_name = "Role"
        verbose_name_plural = "Roles"
