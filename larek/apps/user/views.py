from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from rest_framework import viewsets

from larek.apps.user.forms import UserLoginForm, UserRegistrationForm
from larek.apps.user.models import User
from larek.apps.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRegistrationView(CreateView):
    model = User
    success_url = reverse_lazy("index")
    form_class = UserRegistrationForm


class UserLoginView(LoginView):
    template_name = "login.html"
    next_page = reverse_lazy("index")
    form_class = UserLoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")
