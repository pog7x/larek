from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from larek.apps.cart.models import Cart


class LoginRequiredTemplateView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")


class LoginAndCartsRequiredTemplateView(LoginRequiredTemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not Cart.user_has_carts(user_id=request.user.id):
            return HttpResponseRedirect(reverse_lazy("catalog"))
        return super().dispatch(request, *args, **kwargs)
