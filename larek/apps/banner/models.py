from django.db import models

from larek.apps.product_seller.models import ProductSeller


class BannerProductSeller(models.Model):
    class Type(models.IntegerChoices):
        MAIN_SLIDER = 1
        LIMITED_OFFERS = 2
        POPULAR_GOODS = 3
        LIMITED_EDITION = 4

    product_seller = models.ForeignKey(
        to=ProductSeller,
        null=True,
        on_delete=models.CASCADE,
        related_name="banner_product_seller",
        verbose_name="Product Seller",
    )
    type = models.IntegerField(
        null=True,
        choices=Type.choices,
        verbose_name="Banner Type",
    )
    expired_at = models.DateTimeField(
        null=True,
        verbose_name="Banner Product Expired At",
    )

    def __str__(self):
        return f"{self.type} :: {self.product_seller}"

    class Meta:
        db_table = "banner_product"
        verbose_name = "Banner Product"
        verbose_name_plural = "Banner Product"

    def for_countdown(self):
        return self.expired_at.strftime("%d.%m.%Y %H:%M")

    @property
    def is_main_slider(self):
        return int(self.type) == self.Type.MAIN_SLIDER

    @property
    def is_limited_offers(self):
        return int(self.type) == self.Type.LIMITED_OFFERS

    @property
    def is_popular_goods(self):
        return int(self.type) == self.Type.POPULAR_GOODS

    @property
    def is_limited_edition(self):
        return int(self.type) == self.Type.LIMITED_EDITION
