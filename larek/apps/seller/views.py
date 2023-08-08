from rest_framework import viewsets

from larek.apps.seller.models import Seller
from larek.apps.seller.serializers import SellerSerializer


class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
