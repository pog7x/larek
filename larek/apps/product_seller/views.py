from rest_framework import viewsets

from larek.apps.product_seller.models import ProductSeller
from larek.apps.product_seller.serializers import ProductSellerSerializer


class ProductSellerViewSet(viewsets.ModelViewSet):
    queryset = ProductSeller.objects.all()
    serializer_class = ProductSellerSerializer
