from rest_framework import serializers

from larek.apps.product_seller.models import ProductSeller
from larek.apps.product.serializers import ProductSerializer


class ProductSellerSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = ProductSeller
        fields = "__all__"
        depth = 3
