from django_filters import rest_framework

from larek.apps.cart.models import Cart


class CartFilter(rest_framework.FilterSet):
    class Meta:
        model = Cart
        fields = {"product_seller_id": ["exact"]}
