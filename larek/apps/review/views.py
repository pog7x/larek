from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from larek.apps.review.forms import CreateReviewForm
from larek.apps.review.models import Review


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = CreateReviewForm
    template_name = "review_detail.html"
    login_url = reverse_lazy("login")

    def post(self, request, *args, **kwargs):
        form = self.form_class({**request.POST.dict(), "user_id": request.user.id})
        if form.is_valid():
            self.object = form.save()
            return self.render_to_response({"review": self.object})
        else:
            return HttpResponseBadRequest(form.errors)
