import logging
from typing import Any

from django.core.paginator import InvalidPage
from django.db.models import Count, Sum
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_filters.rest_framework import DjangoFilterBackend
from django_htmx.middleware import HtmxDetails
from rest_framework import filters, pagination, viewsets

from larek.apps.cart.models import Cart
from larek.apps.product_seller.filters import ProductSellerFilter
from larek.apps.product_seller.models import ProductSeller
from larek.apps.product_seller.serializers import ProductSellerSerializer


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


log = logging.getLogger(__name__)


class ProductSellerPagination(pagination.PageNumberPagination):
    page_size = 9


class ProductSellerViewSet(viewsets.ModelViewSet):
    queryset = ProductSeller.objects.prefetch_related(
        "product",
        "product__images",
    ).filter(
        products_count__gt=0,
    )

    ORDERING_VIEWS_HISTORY_COUNT = "popularity"
    ORDERING_REVIEW_COUNT = "product__review__count"
    ORDERING_PRODUCT_ID = "product__id"
    ORDERING_PRICE = "price"

    serializer_class = ProductSellerSerializer
    pagination_class = ProductSellerPagination
    filterset_class = ProductSellerFilter
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = [
        ORDERING_VIEWS_HISTORY_COUNT,
        ORDERING_REVIEW_COUNT,
        ORDERING_PRODUCT_ID,
        ORDERING_PRICE,
    ]

    def get_queryset(self):
        ordering_param: str = self.request.query_params.get("ordering")
        queryset = self.queryset

        if ordering_param:
            if ordering_param.endswith(self.ORDERING_VIEWS_HISTORY_COUNT):
                queryset = queryset.annotate(
                    popularity=Sum("product__views_history__count", default=0)
                )
            elif ordering_param.endswith(self.ORDERING_REVIEW_COUNT):
                queryset = queryset.annotate(Count("product__review"))

        return queryset


from django import forms


class ProductSellerListForm(forms.Form):
    price__gte = forms.IntegerField(required=False)
    price__lte = forms.IntegerField(required=False)
    product__name__icontains = forms.CharField(required=False)


class ProductSellerListView(ListView):
    model = ProductSeller

    ORDERING_POPULARITY = "popularity"
    ORDERING_REVIEW_COUNT = "product__review__count"
    ORDERING_PRODUCT_ID = "product__id"
    ORDERING_PRICE = "price"

    template_name = "catalog_1.html"
    context_object_name = "product_seller_list"
    paginate_by = 8
    ordering = ORDERING_POPULARITY

    queryset = ProductSeller.objects.prefetch_related("product", "product__images")

    ORDERING_MAP = {
        ORDERING_POPULARITY: "Популярности",
        ORDERING_REVIEW_COUNT: "Отзывам",
        ORDERING_PRODUCT_ID: "Новизне",
        ORDERING_PRICE: "Цене",
    }

    def get(self, request: HtmxHttpRequest, *args, **kwargs):
        # if request.htmx:
        #     log.info(f"{request.GET} <===HTMX====GET")
        # else:
        #     log.info(f"{request.GET} <=======")
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.htmx:
            self.template_name = "product_seller.html"
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordering_map"] = self.ORDERING_MAP
        context["active_ordering"] = self.ordering
        return context

    def get_queryset(self):
        price__gte = self.request.GET.get("price__gte") or "1"
        price__lte = self.request.GET.get("price__lte") or "50000"
        product__name__icontains = self.request.GET.get("product__name__icontains", "")
        in_stock = self.request.GET.get("in_stock") == "on"

        self.ordering = self.request.GET.get("ordering") or f"-{self.ordering}"

        queryset = self.queryset.filter(
            price__gte=price__gte,
            price__lte=price__lte,
            product__name__icontains=product__name__icontains,
            products_count__gt=0 if in_stock else -1,
        )

        return self._ordering(queryset)

    def _ordering(self, queryset):
        if ordering := self.get_ordering():
            if ordering.endswith(self.ORDERING_POPULARITY):
                queryset = queryset.annotate(
                    popularity=Sum("product__views_history__count", default=0)
                )
            elif ordering.endswith(self.ORDERING_REVIEW_COUNT):
                queryset = queryset.annotate(Count("product__review"))

            if isinstance(ordering, str):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset

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
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as err:
            raise Http404(f"Invalid page {page_number} {err}.")


class ProductSellerDetailView(DetailView):
    model = ProductSeller
    queryset = ProductSeller.objects.prefetch_related(
        "product", "product__review", "product__product_characteristic"
    )
    template_name = "product_1.html"
