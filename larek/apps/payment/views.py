import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from larek.apps.cart.models import Cart
from larek.apps.order.models import Order
from larek.apps.payment.forms import PaymentProcessForm
from larek.apps.payment.models import Payment
from larek.apps.payment.serializers import PaymentSerializer
from larek.apps.product_seller.models import ProductSeller
from larek.apps.rmq.apps import larek_publisher
from larek.authentication import CustomSessionAuthentication

logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentProcessView(LoginRequiredMixin, UpdateView):
    model = Payment
    login_url = reverse_lazy("login")
    form_class = PaymentProcessForm
    template_name = "payment.html"
    pk_url_kwarg = "payment_id"

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        self.object: Payment = self.model.objects.get(id=pk)
        if self.object.status == Payment.STATUS_PROCESSING:
            return HttpResponseRedirect(reverse_lazy("progresspayment", args=[pk]))
        elif self.object.status == Payment.STATUS_PAID:
            return HttpResponseRedirect(reverse_lazy("orders_history"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        cart_total = Cart.cart_total_for_user_order(
            self.request.user.id, self.object.order_id
        )
        self.object.sum = cart_total[0].get("total_products_price")
        self.object.save()
        return super().get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy("progresspayment", args=[self.object.id])

    def form_valid(self, form):
        try:
            with transaction.atomic():
                form.instance.status = Payment.STATUS_PROCESSING
                ProductSeller.decrease_products_count(order_id=form.instance.order_id)
                Cart.decrease_products_count(order_id=form.instance.order_id)
                larek_publisher.publish(
                    data={Payment.PAYMENT_ID_KWARG: str(form.instance.id)},
                )
                return super().form_valid(form)
        except:
            order = Order.objects.get(id=form.instance.order_id)
            order.status = Order.STATUS_NOT_ACTUAL
            order.save()
            return HttpResponseRedirect(reverse_lazy("orders_history"))


class PaymentWaitView(LoginRequiredMixin, DetailView):
    model = Payment
    login_url = reverse_lazy("login")
    template_name = "progresspayment.html"
    pk_url_kwarg = "payment_id"

    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        self.object: Payment = self.model.objects.get(id=pk)
        if self.object.status == Payment.STATUS_INIT:
            return HttpResponseRedirect(reverse_lazy("payment", args=[pk]))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.object or self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
