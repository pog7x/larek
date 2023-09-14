from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, pagination, viewsets

from larek.apps.product_seller.filters import ProductSellerFilter
from larek.apps.product_seller.models import ProductSeller
from larek.apps.product_seller.serializers import ProductSellerSerializer


class ProductSellerPagination(pagination.PageNumberPagination):
    page_size = 9


class ProductSellerViewSet(viewsets.ModelViewSet):
    queryset = ProductSeller.objects.prefetch_related(
        "product",
        "product__images",
    ).filter(
        products_count__gt=0,
    )

    ORDERING_VIEWS_HISTORY_COUNT = "product__views_history__count"
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
                queryset = queryset.annotate(Count("product__views_history"))
            elif ordering_param.endswith(self.ORDERING_REVIEW_COUNT):
                queryset = queryset.annotate(Count("product__review"))

        return queryset
