from rest_framework import serializers

from larek.apps.product_seller.models import ProductSeller


class ProductSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSeller
        fields = "__all__"
        depth = 3
