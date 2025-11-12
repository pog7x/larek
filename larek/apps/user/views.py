from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from larek.apps.user.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from larek.apps.user.models import User


class UserRegistrationView(CreateView):
    model = User
    success_url = reverse_lazy("index")
    template_name = "registration.html"
    form_class = UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("index")
    form_class = UserLoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")
    http_method_names = ["get", "post", "options"]

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = reverse_lazy("login")
    form_class = UserProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Updated Successfully!"

    def get_object(self):
        return self.request.user


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "password_change.html"
    success_url = reverse_lazy("profile")
    success_message = "Password changed successfully"
