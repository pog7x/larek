from rest_framework import serializers

from larek.apps.cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    product_seller_id = serializers.IntegerField()

    class Meta:
        model = Cart
        fields = ["product_seller", "products_count", "product_seller_id"]
        depth = 2
