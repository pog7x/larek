from django.db import models

from larek.apps.order.models import Order
from larek.apps.product_seller.models import ProductSeller
from larek.apps.user.models import User


class Cart(models.Model):
    products_count = models.IntegerField(
        default=0,
        null=True,
        verbose_name="Products Count",
    )
    user = models.ForeignKey(
        to=User,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="User",
        related_name="cart",
    )
    order = models.ForeignKey(
        to=Order,
        default=None,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Order",
        related_name="cart",
    )
    product_seller = models.ForeignKey(
        to=ProductSeller,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Product Seller",
        related_name="cart",
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Cart Deleted At",
    )

    def __str__(self):
        return f"Cart #{self.id}"

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
