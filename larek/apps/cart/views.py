from rest_framework import viewsets
from larek.apps.cart.models import Cart
from larek.apps.cart.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
