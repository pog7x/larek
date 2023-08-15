from rest_framework import serializers

from larek.apps.product.models import Product
from larek.apps.review.serializers import ReviewSerializer


class ProductSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = ["name", "catalog_category", "description", "product_seller", "review"]
        depth = 2
