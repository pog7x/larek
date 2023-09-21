from rest_framework import viewsets

from larek.apps.delivery.models import Delivery
from larek.apps.delivery.serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
