import logging
from datetime import datetime
from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponseBadRequest, QueryDict
from django.views.generic import CreateView, ListView, TemplateView, View
from django.views.generic.detail import (
    SingleObjectMixin,
    SingleObjectTemplateResponseMixin,
)
from django_filters.rest_framework import DjangoFilterBackend
from django_htmx.http import trigger_client_event
from rest_framework import status, views, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from larek.apps.cart.filters import CartFilter
from larek.apps.cart.forms import CartCreateForm, CartUpdateForm
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
    filterset_class = CartFilter
    filter_backends = [DjangoFilterBackend]

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
        product_seller_id = serializer.data.get("product_seller_id")
        request_count = serializer.data.get("products_count", 0)
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
        request_count = int(serializer.validated_data.get("products_count"))
        serializer.validated_data["products_count"] = self.product_seller_curr_count(
            instance.product_seller_id, request_count
        )
        serializer.save()

    def product_seller_curr_count(self, product_seller_id, request_count):
        try:
            request_count = int(request_count or 0)
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


class CartChangeMixin:
    model = Cart
    TRIGGER_CLIENT_EVENT = "update_cart_total"

    def _fetch_cart(self, product_seller_id):
        try:
            cart = self.model.objects.get(
                product_seller_id=product_seller_id,
                user_id=self.request.user.id,
                deleted_at=None,
                order_id=None,
            )
        except self.model.DoesNotExist:
            cart = None

        return cart

    def _perform_update_or_create(self, form: CartCreateForm, allow_zero_count=False):
        product_seller_id = form.cleaned_data.get("product_seller_id")
        request_count = form.cleaned_data.get("products_count", 1)
        user_id = form.cleaned_data.get("user_id")

        products_count = self._product_seller_curr_count(
            product_seller_id, request_count
        )

        if products_count <= 0 and not allow_zero_count:
            return

        if cart := self._fetch_cart(product_seller_id):
            cart.products_count = products_count
        else:
            cart = self.model(
                product_seller_id=product_seller_id,
                products_count=products_count,
                user_id=user_id,
            )

        cart.save()

        return cart

    def _product_seller_curr_count(self, product_seller_id, request_count):
        try:
            request_count = int(request_count or 0)
            product_seller = ProductSeller.objects.get(id=product_seller_id)

            if request_count > product_seller.products_count:
                return product_seller.products_count
            elif request_count < 1:
                return 1

            return request_count
        except ProductSeller.DoesNotExist:
            raise ValueError("product_seller_id is not found")


class CartCreateView(CartChangeMixin, CreateView):
    model = Cart
    form_class = CartCreateForm
    template_name = "change_cart.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class({**request.POST.dict(), "user_id": request.user.id})

        if form.is_valid():
            self.object = self._perform_update_or_create(form)
            return trigger_client_event(
                response=self.render_to_response(
                    context={
                        "cart": self.object,
                        "product_seller_id": form.cleaned_data.get("product_seller_id"),
                    },
                ),
                name=self.TRIGGER_CLIENT_EVENT,
            )
        else:
            return HttpResponseBadRequest(form.errors)

    def get_context_data(self, **kwargs):
        product_seller_id = self.request.GET.get("product_seller_id")

        if not product_seller_id:
            return HttpResponseBadRequest("idi nahuy")

        return super().get_context_data(
            cart=self._fetch_cart(product_seller_id),
            product_seller_id=product_seller_id,
            **kwargs,
        )


class CartItemView(
    SingleObjectMixin,
    CartChangeMixin,
    SingleObjectTemplateResponseMixin,
    View,
):
    model = Cart
    template_name = "change_cart.html"

    def delete(self, request, *args, **kwargs):
        self.object: Cart = self.get_object()
        self._perform_deleted_at(self.object)
        product_seller_id = self.object.product_seller.id
        return trigger_client_event(
            response=self.render_to_response(
                context={
                    "cart": self._fetch_cart(product_seller_id),
                    "product_seller_id": product_seller_id,
                },
            ),
            name=self.TRIGGER_CLIENT_EVENT,
        )

    def put(self, request, *args, **kwargs):
        self.object: Cart = self.get_object()
        form = CartUpdateForm(QueryDict(request.body).dict(), instance=self.object)
        product_seller_id = self.object.product_seller.id

        if form.is_valid():
            products_count = form.cleaned_data["products_count"]
        else:
            products_count = 1

        self.object.products_count = self._product_seller_curr_count(
            product_seller_id, products_count
        )

        self.object.save()
        return trigger_client_event(
            response=self.render_to_response(
                context={
                    "cart": self.object,
                    "product_seller_id": product_seller_id,
                },
            ),
            name=self.TRIGGER_CLIENT_EVENT,
        )

    def _perform_deleted_at(self, instance: Cart):
        instance.deleted_at = datetime.now()
        instance.save()
        return instance


class CartListView(ListView):
    model = Cart
    queryset = Cart.objects.prefetch_related(
        "product_seller",
        "product_seller__seller",
        "product_seller__product",
        "product_seller__product__images",
    ).filter(
        deleted_at=None,
        order_id=None,
    )
    template_name = "cart_1.html"

    def get_queryset(self) -> QuerySet[Any]:
        self.queryset = self.queryset.filter(user_id=self.request.user.id)
        return super().get_queryset()


class CartTotalHeaderView(TemplateView):
    template_name = "cart_total_header.html"
    DEFAULT_RES = {"total_products_count": 0, "total_products_price": 0}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        res = Cart.cart_total_for_user(self.request.user.id)
        return super().get_context_data(
            **(res[0] if res else self.DEFAULT_RES), **kwargs
        )


class CartTotalListView(TemplateView):
    template_name = "cart_total_list.html"
    DEFAULT_RES = {"total_products_count": 0, "total_products_price": 0}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        res = Cart.cart_total_for_user(self.request.user.id)
        return super().get_context_data(
            **(res[0] if res else self.DEFAULT_RES), **kwargs
        )
