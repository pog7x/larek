from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from larek.apps.cart.models import Cart


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")


class LoginAndCartsRequiredTemplateView(LoginRequiredTemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not self.check_carts_is_not_empty():
            return HttpResponseRedirect(reverse_lazy("catalog"))
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def check_carts_is_not_empty(self):
        carts = Cart.objects.filter(
            user_id=self.request.user.id,
            deleted_at=None,
            order_id=None,
        )
        return carts
