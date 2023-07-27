from django.db import models

from larek.apps.product.models import Product
from larek.apps.user.models import User


class ViewsHistory(models.Model):
    product = models.ForeignKey(
        to=Product,
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

    class Meta:
        db_table = "views_history"
