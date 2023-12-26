import json

from django.db import models, transaction
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from larek.apps.cart.models import Cart
from larek.apps.delivery.models import Delivery
from larek.apps.order.forms import OrderCreateForm
from larek.apps.order.models import Order
from larek.apps.payment.models import Payment


class BaseOrdersHistoryView:
    model = Order

    def get_queryset(self):
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


class OrdersHistoryView(LoginRequiredMixin, BaseOrdersHistoryView, ListView):
    template_name = "orders_history.html"
    login_url = reverse_lazy("login")


class OrderDetailView(LoginRequiredMixin, BaseOrdersHistoryView, DetailView):
    template_name = "order_item.html"
    login_url = reverse_lazy("login")


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderCreateForm
    template_name = "order_create.html"
    login_url = reverse_lazy("login")

    def post(self, request: HttpRequest, *args: str, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            if payment_id := self.perform_create(form):
                return HttpResponseRedirect(reverse("payment", args=[payment_id]))
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
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
            kwargs.update(
                {
                    "data": {
                        **self.request.POST.dict(),
                        "user_id": self.request.user.id,
                    },
                    "files": self.request.FILES,
                }
            )
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
