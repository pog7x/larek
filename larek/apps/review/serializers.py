from rest_framework import serializers

from larek.apps.review.models import Review
from larek.apps.user.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    user = UserSerializer(required=False)
    created_at = serializers.DateTimeField(required=False, format="%d %B %Y %H:%M")

    class Meta:
        model = Review
        fields = ["user_id", "product_id", "user", "comment", "created_at"]
