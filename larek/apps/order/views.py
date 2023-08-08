from rest_framework import viewsets

from larek.apps.order.models import Order
from larek.apps.order.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
