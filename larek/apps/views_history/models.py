from django.db import models

from larek.apps.product_seller.models import ProductSeller
from larek.apps.user.models import User


class ViewsHistory(models.Model):
    product_seller = models.ForeignKey(
        to=ProductSeller,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        verbose_name="Product",
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

    def __str__(self):
        return f"{self.user} - {self.product}"

    class Meta:
        db_table = "views_history"
        verbose_name = "Views History"
        verbose_name_plural = "Views History"
