from django.db import models


class CatalogCategory(models.Model):
    name = models.TextField(
        max_length=30,
        verbose_name="Category Name",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "catalog_category"
        verbose_name = "Catalog Category"
        verbose_name_plural = "Catalog Categories"
