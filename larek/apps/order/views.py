import logging
from typing import Any

from django.db import transaction
from django.db.models.query import QuerySet
from django.urls import reverse
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from larek.apps.cart.models import Cart
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
        payment_id = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        headers["Location"] = reverse("payment", args=[payment_id])

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
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


class HistoryOrderView(ListView):
    model = Order
    template_name = "historyorder.html"

    def get_queryset(self) -> QuerySet[Any]:
        qs = (
            Order.objects.prefetch_related("payment")
            .filter(user_id=self.request.user.id)
            .order_by("-id")
        )
        return qs


class OrderDetailView(DetailView):
    model = Order
    template_name = "oneorder.html"

    def get_queryset(self) -> QuerySet[Any]:
        qs = Order.objects.prefetch_related(
            "payment",
            "cart",
        ).filter(user_id=self.request.user.id)
        return qs
