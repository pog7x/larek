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
    comment = models.TextField(null=True, verbose_name="Review Comment")
    created_at = models.DateTimeField(null=True, auto_now_add=True)

    def __str__(self):
        return f"{self.comment[:30]}..." if self.comment else ""

    class Meta:
        db_table = "review"
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        ordering = ["id"]
