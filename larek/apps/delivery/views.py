from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from larek.apps.delivery.models import Delivery
from larek.apps.delivery.serializers import DeliverySerializer
from larek.authentication import CustomSessionAuthentication


class DeliveryViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
