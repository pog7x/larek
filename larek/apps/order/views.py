import json
import logging
from typing import Any

from django.db import models, transaction
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from larek.apps.cart.models import Cart
from larek.apps.delivery.models import Delivery
from larek.apps.order.forms import OrderCreateForm
from larek.apps.order.models import Order
from larek.apps.order.serializers import OrderSerializer
from larek.apps.payment.models import Payment
from larek.authentication import CustomSessionAuthentication
from larek.permissions import UserHasCartPermission

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated, UserHasCartPermission)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["user_id"] = request.user.id
        if payment_id := self.perform_create(serializer):
            headers = self.get_success_headers(serializer.data)
            headers["Location"] = reverse("payment", args=[payment_id])

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            return Response(
                data={"error": "validation error"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        user_id = self.request.user.id
        cart_total = Cart.cart_total_for_user(user_id)
        if cart_total and cart_total[0].get("total_products_count", 0) != 0:
            with transaction.atomic():
                order = Order(**serializer.data)
                order.save()
                payment = Payment(
                    order=order,
                    sum=cart_total[0].get("total_products_price"),
                )
                payment.save()
                Cart.objects.filter(
                    user_id=user_id,
                    order_id=None,
                    deleted_at=None,
                ).update(order_id=order.id)

                return payment.id


class BaseOrdersHistoryView:
    model = Order

    def get_queryset(self) -> QuerySet[Any]:
        return (
            Order.objects.prefetch_related("payment", "cart", "cart__product_seller")
            .filter(user_id=self.request.user.id)
            .annotate(
                total_products_price=models.Sum(
                    models.F("cart__products_count")
                    * models.F("cart__product_seller__price")
                )
            )
            .order_by("-id")
        )


class OrdersHistoryView(BaseOrdersHistoryView, ListView):
    template_name = "orders_history.html"


class OrderDetailView(BaseOrdersHistoryView, DetailView):
    template_name = "oneorder.html"


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order_create.html"

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = None
        form = self.get_form()
        if form.is_valid():
            if payment_id := self.perform_create(form):
                return HttpResponseRedirect(reverse("payment", args=[payment_id]))
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        carts = Cart.objects.filter(
            user_id=self.request.user.id, deleted_at=None, order_id=None
        )
        cart_total = Cart.cart_total_for_user(self.request.user.id)
        deliveries = Delivery.objects.all()
        deliveries_json = json.dumps({object.id: str(object) for object in deliveries})
        return super().get_context_data(
            carts=carts,
            deliveries=deliveries,
            deliveries_json=deliveries_json,
            **cart_total,
            **kwargs,
        )

    def get_form_kwargs(self):
        kwargs = {
            "initial": self.get_initial(),
            "prefix": self.get_prefix(),
        }

        if self.request.method in ("POST", "PUT"):
            kwargs.update({
                "data": {
                    **self.request.POST.dict(),
                    "user_id": self.request.user.id,
                },
                "files": self.request.FILES,
            })
        return kwargs

    def perform_create(self, form: OrderCreateForm):
        user_id = self.request.user.id
        cart_total = Cart.cart_total_for_user(user_id)
        if cart_total and cart_total.get("total_products_count", 0) != 0:
            with transaction.atomic():
                order = Order(**form.cleaned_data)
                order.save()
                payment = Payment(
                    order=order,
                    sum=cart_total.get("total_products_price"),
                )
                payment.save()
                Cart.objects.filter(
                    user_id=user_id,
                    order_id=None,
                    deleted_at=None,
                ).update(order_id=order.id)

                return payment.id
