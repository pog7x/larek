from rest_framework import viewsets

from larek.apps.role.models import Role
from larek.apps.role.serializers import RoleSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
