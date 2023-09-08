from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from larek.apps.role.models import Role


def avatar_image_directory_path(instance: "User", filename):
    return f"user/avatars/{instance.pk}/{int(datetime.now().timestamp())}{filename}"


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
    avatar = models.FileField(
        null=True,
        blank=True,
        upload_to=avatar_image_directory_path,
    )

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
