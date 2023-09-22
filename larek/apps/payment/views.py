from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from rest_framework import viewsets
from django.http import HttpResponseRedirect
import logging
from larek.apps.payment.models import Payment
from larek.apps.payment.serializers import PaymentSerializer
from larek.apps.payment.forms import PaymentProcessForm


logger = logging.getLogger(__name__)


class PaymentViewSet(viewsets.ModelViewSet):
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
        payment: Payment = self.model.objects.get(id=pk)
        if payment.status == Payment.STATUS_PROCESSING:
            return HttpResponseRedirect(reverse_lazy("progresspayment", args=[pk]))
        elif payment.status in (Payment.STATUS_ERROR, Payment.STATUS_PAID):
            return HttpResponseRedirect(reverse_lazy("historyorder"))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy("progresspayment", args=[self.object.id])

    def form_valid(self, form):
        form.instance.status = Payment.STATUS_PROCESSING
        self.object = form.save()
        return super().form_valid(form)
