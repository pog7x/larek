from typing import Any

from larek.apps.catalog_category.models import CatalogCategory


class CatalogCategoryCtx:
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return {"catalog_categories": CatalogCategory.objects.all()}


catalog_categories = CatalogCategoryCtx()
