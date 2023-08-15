from rest_framework import viewsets

from larek.apps.product.models import Product
from larek.apps.product.serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("product_seller", "review")
    serializer_class = ProductSerializer
