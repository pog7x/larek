from django.core.paginator import InvalidPage
from django.db.models import Count, Sum
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from larek.apps.product_seller.models import ProductSeller


class ProductSellerListView(ListView):
    ORDERING_POPULARITY = "popularity"
    ORDERING_REVIEW_COUNT = "product__review__count"
    ORDERING_ID = "id"
    ORDERING_PRICE = "price"

    ORDERING_MAP = {
        ORDERING_POPULARITY: "Популярности",
        ORDERING_REVIEW_COUNT: "Отзывам",
        ORDERING_ID: "Новизне",
        ORDERING_PRICE: "Цене",
    }

    model = ProductSeller
    template_name = "catalog.html"
    paginate_by = 8
    ordering = ORDERING_POPULARITY
    queryset = ProductSeller.objects.prefetch_related("product", "product__images")

    def get(self, request, *args, **kwargs):
        self.ordering = self.request.GET.get("ordering") or f"-{self.ordering}"
        return super().get(request, *args, **kwargs)

    def get_template_names(self):
        if self.request.htmx:
            self.template_name = "product_seller_list.html"
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ordering_map"] = self.ORDERING_MAP
        context["active_ordering"] = self.ordering
        return context

    def get_queryset(self):
        price_gte = self.request.GET.get("price_gte") or "1"
        price_lte = self.request.GET.get("price_lte") or "50000"
        product_name = self.request.GET.get("product_name", "")
        in_stock = self.request.GET.get("in_stock") == "on"
        catalog_category = self.request.GET.get("catalog_category")

        queryset = self.queryset.filter(
            price__gte=price_gte,
            price__lte=price_lte,
            product__name__icontains=product_name,
            products_count__gt=0 if in_stock else -1,
        )

        if catalog_category:
            queryset = queryset.filter(
                product__catalog_category__id=catalog_category,
            )

        return self._ordering(queryset)

    def _ordering(self, queryset):
        if ordering := self.get_ordering():
            if ordering.endswith(self.ORDERING_POPULARITY):
                queryset = queryset.annotate(
                    popularity=Sum("views_history__count", default=0)
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
    template_name = "product_seller_detail.html"
