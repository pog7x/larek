from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from larek.apps.review.models import Review
from larek.apps.review.serializers import ReviewSerializer
from larek.authentication import CustomSessionAuthentication


class ReviewViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.id
        return super().create(request, *args, **kwargs)
