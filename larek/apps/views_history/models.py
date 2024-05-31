from django.db import models

from larek.apps.product_seller.models import ProductSeller
from larek.apps.user.models import User


class ViewsHistory(models.Model):
    product_seller = models.ForeignKey(
        to=ProductSeller,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Product Seller",
        related_name="views_history",
    )
    user = models.ForeignKey(
        to=User,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="views_history",
    )
    count = models.IntegerField(
        default=1,
        null=True,
        verbose_name="Count",
    )
    updated_at = models.DateTimeField(
        null=True,
        auto_now=True,
        verbose_name="Updated At",
    )

    def __str__(self):
        return f"{self.user} - {self.product_seller}"

    class Meta:
        db_table = "views_history"
        verbose_name = "Views History"
        verbose_name_plural = "Views History"
