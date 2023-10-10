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

    @classmethod
    def cart_total_for_user(cls, user_id):
        return (
            cls.objects.prefetch_related("product_seller")
            .filter(
                user_id=user_id,
                order_id=None,
                deleted_at=None,
            )
            .values("user_id")
            .annotate(total_products_count=models.Sum("products_count"))
            .annotate(
                total_products_price=models.Sum(
                    models.F("products_count") * models.F("product_seller__price")
                )
            )
        )

    @classmethod
    def user_has_carts(cls, user_id):
        return bool(
            cls.objects.filter(
                user_id=user_id,
                deleted_at=None,
                order_id=None,
            )
        )

    def __str__(self):
        return f"Cart #{self.id}"

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["id"]
