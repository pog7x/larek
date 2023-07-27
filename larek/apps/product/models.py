from django.db import models

from larek.apps.catalog_category.models import CatalogCategory


class Product(models.Model):
    name = models.TextField(
        max_length=30,
        null=True,
        verbose_name="Product Name",
    )
    catalog_category = models.ForeignKey(
        to=CatalogCategory,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Catalog Category",
        related_name="product",
    )
    description = models.TextField(
        max_length=999,
        null=True,
        verbose_name="Description",
    )

    class Meta:
        db_table = "product"
