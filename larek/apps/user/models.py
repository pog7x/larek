from django.contrib.auth.models import AbstractUser
from django.db import models

from larek.apps.role.models import Role


class User(AbstractUser):
    role = models.ForeignKey(
        to=Role,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Role",
        related_name="user",
    )
    phone = models.TextField(
        null=True,
        verbose_name="User Phone",
    )
    address = models.TextField(
        null=True,
        verbose_name="User Address",
    )

    class Meta:
        db_table = "user"
