from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from larek.apps.cart.models import Cart
from larek.apps.order.models import Order
from larek.apps.payment.forms import PaymentProcessForm
from larek.apps.payment.models import Payment
from larek.apps.product_seller.models import ProductSeller


class PaymentInitView(LoginRequiredMixin, UpdateView):
    model = Payment
    login_url = reverse_lazy("login")
    form_class = PaymentProcessForm
    template_name = "payment.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status == Payment.STATUS_PROCESSING:
            return HttpResponseRedirect(
                reverse_lazy("payment_progress", args=[self.object.id])
            )
        elif self.object.status == Payment.STATUS_PAID:
            return HttpResponseRedirect(reverse_lazy("orders_history"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cart_total = Cart.cart_total_for_user_order(
            self.request.user.id, self.object.order_id
        )
        self.object.sum = cart_total[0].get("total_products_price")
        self.object.save()
        return super().get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy("payment_progress", args=[self.object.id])

    def form_valid(self, form):
        try:
            with transaction.atomic():
                form.instance.status = Payment.STATUS_PROCESSING
                ProductSeller.decrease_products_count(order_id=form.instance.order_id)
                Cart.decrease_products_count(order_id=form.instance.order_id)
                return super().form_valid(form)
        except:
            order = Order.objects.get(id=form.instance.order_id)
            order.status = Order.STATUS_NOT_ACTUAL
            order.save()
            return HttpResponseRedirect(reverse_lazy("orders_history"))


class PaymentProgressView(LoginRequiredMixin, DetailView):
    model = Payment
    login_url = reverse_lazy("login")
    template_name = "payment_progress.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.status == Payment.STATUS_INIT:
            return HttpResponseRedirect(reverse_lazy("payment", args=[self.object.id]))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_template_names(self):
        if self.request.htmx:
            self.template_name = "payment_wait.html"
        return super().get_template_names()
