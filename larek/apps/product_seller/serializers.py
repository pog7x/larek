from rest_framework import serializers

from larek.apps.product.serializers import ProductBaseSerializer
from larek.apps.product_seller.models import ProductSeller


class ProductSellerSerializer(serializers.ModelSerializer):
    product = ProductBaseSerializer()

    class Meta:
        model = ProductSeller
        fields = "__all__"
        depth = 3
