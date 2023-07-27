from django.db import models

from larek.apps.product.models import Product
from larek.apps.user.models import User


class Review(models.Model):
    product = models.ForeignKey(
        to=Product,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Product",
        related_name="review",
    )
    user = models.ForeignKey(
        to=User,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="review",
    )
    comment = models.TextField(max_length=999, null=True, verbose_name="Review Comment")

    class Meta:
        db_table = "review"
