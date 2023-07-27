from django.db import models


class CatalogCategory(models.Model):
    name = models.TextField(
        max_length=30,
        verbose_name="Category Name",
    )

    class Meta:
        db_table = "catalog_category"
