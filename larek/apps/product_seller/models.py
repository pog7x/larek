from django.db import connection, models

from larek.apps.product.models import Product
from larek.apps.seller.models import Seller


class ProductSeller(models.Model):
    product = models.ForeignKey(
        to=Product,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Product",
        related_name="product_seller",
    )
    seller = models.ForeignKey(
        to=Seller,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Seller",
        related_name="product_seller",
    )
    products_count = models.PositiveIntegerField(
        default=0,
        null=True,
        verbose_name="Products Count",
    )
    price = models.FloatField(
        default=0,
        null=True,
        verbose_name="Price",
    )

    def __str__(self):
        return f"#{self.id} | Seller #{self.seller.id} Product {str(self.product)}"

    class Meta:
        db_table = "product_seller"
        verbose_name = "Product Seller"
        verbose_name_plural = "Product Seller"

    @classmethod
    def decrease_products_count(cls, order_id):
        with connection.cursor() as cursor:
            # fmt: off
            cursor.execute(
                f"""
                    UPDATE product_seller AS p_s 
                    SET products_count = p_s.products_count - ca.products_count 
                    FROM cart AS ca 
                    WHERE ca.product_seller_id = p_s.id AND ca.order_id = {order_id};
                """
            )
