from larek.apps.catalog_category.models import CatalogCategory


class CatalogCategoryCtx:
    def __call__(self, *args, **kwargs):
        return {"catalog_categories": CatalogCategory.objects.all()}


catalog_categories = CatalogCategoryCtx()
