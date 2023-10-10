from django.db import models

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
    products_count = models.IntegerField(
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
        return (
            f"{self.seller} sells {self.product}, price: {self.price}, count:"
            f" {self.products_count}"
        )

    class Meta:
        db_table = "product_seller"
        verbose_name = "Product Seller"
        verbose_name_plural = "Product Seller"
