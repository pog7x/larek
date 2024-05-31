from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import InvalidPage
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView

from larek.apps.views_history.models import ViewsHistory


class ViewsHistoryListView(LoginRequiredMixin, ListView):
    model = ViewsHistory
    queryset = ViewsHistory.objects.prefetch_related(
        "product_seller",
        "product_seller__seller",
        "product_seller__product",
        "product_seller__product__images",
    ).order_by("-updated_at")
    template_name = "views_history.html"
    login_url = reverse_lazy("login")
    paginate_by = 4

    def get_queryset(self):
        self.queryset = self.queryset.filter(user_id=self.request.user.id)
        return super().get_queryset()

    def get_template_names(self):
        if self.request.htmx:
            self.template_name = "views_history_list.html"
        return super().get_template_names()

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        len_objects = len(self.object_list)
        max_page = (
            int(len_objects / self.paginate_by) + (len_objects % self.paginate_by > 0)
        ) or 1

        try:
            page_number = int(page)
            page_number = max_page if page_number > max_page else page_number
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                raise Http404("Page is not “last”, not can it be converted to an int.")
        try:
            page = paginator.page(page_number)
            return paginator, page, page.object_list, page.has_other_pages()
        except InvalidPage as err:
            raise Http404(f"Invalid page {page_number} {err}.")
