from rest_framework import viewsets

from larek.apps.catalog_category.models import CatalogCategory
from larek.apps.catalog_category.serializers import CatalogCategorySerializer


class CatalogCategoryViewSet(viewsets.ModelViewSet):
    queryset = CatalogCategory.objects.all()
    serializer_class = CatalogCategorySerializer
