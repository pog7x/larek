from django.contrib.auth.models import AbstractUser
from django.db import models


def avatar_image_directory_path(instance: "User", filename):
    return f"user/avatars/{instance.pk}/{filename}"


class User(AbstractUser):
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
        default="user/default_avatar.svg",
        verbose_name="User Avatar",
    )

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"
