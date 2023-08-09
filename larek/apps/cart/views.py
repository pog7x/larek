from rest_framework import viewsets

from larek.apps.cart.models import Cart
from larek.apps.cart.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.prefetch_related("product_seller")
    serializer_class = CartSerializer
