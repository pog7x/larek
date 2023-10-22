import logging

from django.db import connection, models

from larek.apps.order.models import Order
from larek.apps.payment.models import Payment
from larek.apps.product_seller.models import ProductSeller
from larek.apps.user.models import User

log = logging.getLogger(__name__)


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

    @classmethod
    def decrease_products_count(cls, order_id):
        # fmt: off
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    UPDATE cart AS cart_upd 
                    SET products_count = p_s.products_count 
                    FROM cart 
                    INNER JOIN product_seller AS p_s ON cart.product_seller_id = p_s.id 
                    INNER JOIN cart AS cart_order ON cart_order.product_seller_id = p_s.id 
                    LEFT JOIN payment AS pmnt ON pmnt.order_id = cart.order_id 
                    WHERE cart_upd.product_seller_id = p_s.id 
                    AND cart_order.order_id = {order_id} 
                    AND (cart_upd.order_id IS null OR pmnt.status IN ({Payment.STATUS_INIT},{Payment.STATUS_ERROR})) 
                    AND cart_order.order_id <> COALESCE(cart_upd.order_id,0) 
                    AND cart_upd.products_count > p_s.products_count;
                """
            )

    def __str__(self):
        return f"Cart #{self.id}"

    class Meta:
        db_table = "cart"
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
        ordering = ["id"]
