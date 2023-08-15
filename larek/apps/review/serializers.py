from rest_framework import serializers

from larek.apps.review.models import Review
from larek.apps.user.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    user = UserSerializer(required=False)

    class Meta:
        model = Review
        fields = ["user_id", "product_id", "user", "comment"]
