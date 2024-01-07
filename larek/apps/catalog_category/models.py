from django.db import models


def catalog_category_icon_directory_path(instance: "CatalogCategory", filename):
    return f"catalog_category/icons/{instance.pk}/{filename}"


class CatalogCategory(models.Model):
    name = models.TextField(
        max_length=30,
        verbose_name="Catalog Category Name",
    )
    icon = models.FileField(
        null=True,
        blank=True,
        upload_to=catalog_category_icon_directory_path,
        verbose_name="Catalog Category Icon",
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_image = self.icon
            self.icon = None
            super().save(*args, **kwargs)
            self.icon = saved_image
            self.save()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "catalog_category"
        verbose_name = "Catalog Category"
        verbose_name_plural = "Catalog Categories"
        ordering = ["name"]
