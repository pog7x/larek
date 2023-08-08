from rest_framework import viewsets

from larek.apps.views_history.models import ViewsHistory
from larek.apps.views_history.serializers import ViewsHistorySerializer


class ViewsHistoryViewSet(viewsets.ModelViewSet):
    queryset = ViewsHistory.objects.all()
    serializer_class = ViewsHistorySerializer
