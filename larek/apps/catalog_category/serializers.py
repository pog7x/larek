from rest_framework import serializers

from larek.apps.catalog_category.models import CatalogCategory


class CatalogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogCategory
        fields = "__all__"
