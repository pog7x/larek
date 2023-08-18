from rest_framework import serializers

from larek.apps.cart.models import Cart
from larek.apps.product_seller.serializers import ProductSellerSerializer


class CartSerializer(serializers.ModelSerializer):
    product_seller_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    product_seller = ProductSellerSerializer(required=False)

    class Meta:
        model = Cart
        fields = ["product_seller", "products_count", "product_seller_id", "user_id"]
        depth = 2
