from django.db import models


class Seller(models.Model):
    name = models.TextField(
        max_length=30,
        null=True,
        verbose_name="Seller Name",
    )
    phone = models.TextField(
        max_length=30,
        null=True,
        verbose_name="Seller Phone",
    )
    address = models.TextField(
        max_length=100,
        null=True,
        verbose_name="Seller Address",
    )
    email = models.TextField(
        max_length=30,
        null=True,
        verbose_name="Seller Email",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "seller"
        verbose_name = "Seller"
        verbose_name_plural = "Sellers"
