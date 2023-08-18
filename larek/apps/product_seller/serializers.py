from rest_framework import serializers

from larek.apps.product.serializers import ProductSerializer
from larek.apps.product_seller.models import ProductSeller


class ProductSellerSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductSeller
        fields = "__all__"
        depth = 3
