import logging
from datetime import datetime

from rest_framework import status, views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from larek.apps.cart.models import Cart
from larek.apps.cart.serializers import CartSerializer, CartTotalSerializer
from larek.apps.product_seller.models import ProductSeller
from larek.authentication import CustomSessionAuthentication

logger = logging.getLogger(__name__)


class CartViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.prefetch_related("product_seller")
    serializer_class = CartSerializer

    def get_queryset(self):
        return self.queryset.filter(
            user_id=self.request.user.id,
            deleted_at=None,
            order_id=None,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.perform_update_or_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            CartSerializer(instance=cart).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_deleted_at(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(instance, serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update_or_create(self, serializer):
        product_seller_id = serializer.data["product_seller_id"]
        request_count = int(serializer.data["products_count"])
        user_id = self.request.user.id
        products_count = self.product_seller_curr_count(
            product_seller_id, request_count
        )

        try:
            cart = Cart.objects.get(
                order_id=None,
                deleted_at=None,
                product_seller_id=product_seller_id,
                user_id=user_id,
            )
            setattr(cart, "products_count", products_count)
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart(
                product_seller_id=product_seller_id,
                products_count=products_count,
                user_id=user_id,
            )
            cart.save()

        return cart

    def perform_deleted_at(self, instance: Cart):
        instance.deleted_at = datetime.now()
        instance.save()

    def perform_update(self, instance, serializer):
        request_count = int(serializer.validated_data["products_count"])
        serializer.validated_data["products_count"] = self.product_seller_curr_count(
            instance.product_seller_id, request_count
        )
        serializer.save()

    def product_seller_curr_count(self, product_seller_id, request_count):
        try:
            product_seller = ProductSeller.objects.get(id=product_seller_id)
            if request_count > product_seller.products_count:
                return product_seller.products_count
            elif request_count < 1:
                return 1
            return request_count
        except ProductSeller.DoesNotExist:
            raise ValidationError({"product_seller_id": ["Not found."]})


class CartTotalView(views.APIView):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Cart.objects.prefetch_related("product_seller")
    DEFAULT_RES = {"total_products_count": 0, "total_products_price": 0}

    def get(self, request, format=None):
        res = Cart.cart_total_for_user(request.user.id)
        serializer = CartTotalSerializer(data=res[0] if len(res) else self.DEFAULT_RES)
        serializer.is_valid()
        return Response(serializer.data)
