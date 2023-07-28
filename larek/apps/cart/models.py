from django.db import models

from larek.apps.order.models import Order
from larek.apps.product.models import Product
from larek.apps.seller.models import Seller
from larek.apps.user.models import User


class Cart(models.Model):
    products_count = models.IntegerField(
        default=0,
        null=True,
        verbose_name="Products Count",
    )
    product = models.ForeignKey(
        to=Product,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Product",
        related_name="cart",
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
    seller = models.ManyToManyField(
        to=Seller,
        default=None,
        verbose_name="Seller",
        related_name="cart",
    )

    def __str__(self):
        return f"Cart #{self.id}"

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
