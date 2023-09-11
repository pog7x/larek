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
        null=True,
        verbose_name="Description",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "product"
        verbose_name = "Product"
        verbose_name_plural = "Products"


def product_image_directory_path(instance: "ProductImage", filename):
    return f"product/images/{instance.product.pk}/{filename}"


class ProductImage(models.Model):
    name = models.CharField(
        max_length=128,
        null=False,
        blank=True,
        verbose_name="Product Image Name",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Product",
    )
    image = models.FileField(
        null=True,
        upload_to=product_image_directory_path,
        verbose_name="Product Image",
    )

    def __str__(self):
        return f"{self.name} | {self.product}"

    class Meta:
        db_table = "product_image"
        verbose_name = "Product image"
        verbose_name_plural = "Product images"
        ordering = ["pk"]
