import logging

from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from larek.apps.cart.models import Cart
from larek.apps.order.models import Order
from larek.apps.order.serializers import OrderSerializer
from larek.apps.payment.models import Payment
from larek.authentication import CustomSessionAuthentication

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user_id"] = request.user.id
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        cart_total = Cart.cart_total_for_user(self.request.user.id)
        if cart_total and cart_total[0].get("total_products_count", 0) != 0:
            with transaction.atomic():
                order = Order(**serializer.data)
                order.save()
                payment = Payment(
                    order=order,
                    sum=cart_total[0].get("total_products_price"),
                )
                payment.save()
