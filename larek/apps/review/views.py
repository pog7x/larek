import logging

from django.http import HttpResponseBadRequest
from django.views.generic.edit import CreateView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from larek.apps.review.forms import CreateReviewForm
from larek.apps.review.models import Review
from larek.apps.review.serializers import ReviewSerializer
from larek.authentication import CustomSessionAuthentication

log = logging.getLogger(__name__)


class ReviewViewSet(viewsets.ModelViewSet):
    authentication_classes = (CustomSessionAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.id
        return super().create(request, *args, **kwargs)


class ReviewCreateView(CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = "review_detail.html"

    def post(self, request, *args, **kwargs):
        if request.htmx:
            log.info(f"{request.POST} {self.request.user.id}<<<<HTMX review")
        else:
            log.info(f"{request.POST} <<<< review")
        self.object = None

        form = self.form_class({**request.POST.dict(), "user_id": request.user.id})
        if form.is_valid():
            self.object = form.save()
            return self.render_to_response({"review": self.object})
        else:
            return HttpResponseBadRequest(form.errors)
