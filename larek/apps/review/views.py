from rest_framework import viewsets

from larek.apps.review.models import Review
from larek.apps.review.serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
