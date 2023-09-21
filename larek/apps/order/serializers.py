from rest_framework import serializers

from larek.apps.delivery.serializers import DeliverySerializer
from larek.apps.order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(required=False)
    delivery_id = serializers.IntegerField(required=False)
    delivery = DeliverySerializer(required=False)

    class Meta:
        model = Order
        fields = [
            "full_name",
            "phone",
            "email",
            "address",
            "delivery_id",
            "delivery",
            "user_id",
        ]
