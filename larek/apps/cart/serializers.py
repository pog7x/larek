from rest_framework import serializers

from larek.apps.cart.models import Cart
from larek.apps.product_seller.serializers import ProductSellerSerializer


class CartSerializer(serializers.ModelSerializer):
    product_seller_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)
    product_seller = ProductSellerSerializer(required=False)

    class Meta:
        model = Cart
        fields = [
            "id",
            "product_seller",
            "products_count",
            "product_seller_id",
            "user_id",
        ]


class CartTotalSerializer(serializers.Serializer):
    total_products_count = serializers.IntegerField()
    total_products_price = serializers.IntegerField()
