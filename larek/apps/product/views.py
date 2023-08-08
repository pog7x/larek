from rest_framework import viewsets

from larek.apps.product.models import Product
from larek.apps.product.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
