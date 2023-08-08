from rest_framework import serializers

from larek.apps.user.models import User


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
