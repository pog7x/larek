from rest_framework import serializers

from larek.apps.views_history.models import ViewsHistory


class ViewsHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewsHistory
        fields = "__all__"
