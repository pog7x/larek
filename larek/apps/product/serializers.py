from rest_framework import serializers

from larek.apps.product.models import Product, ProductImage
from larek.apps.review.serializers import ReviewSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["name", "image"]


class ProductBaseSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "catalog_category", "description", "images"]
        depth = 2


class ProductSerializer(serializers.ModelSerializer):
    review = ReviewSerializer(required=False, many=True)
    images = ProductImageSerializer(required=False, many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "catalog_category",
            "description",
            "product_seller",
            "review",
            "images",
        ]
        depth = 2
