from rest_framework import viewsets

from larek.apps.user.models import User
from larek.apps.user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
