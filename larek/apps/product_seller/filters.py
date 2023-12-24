from django_filters import FilterSet, rest_framework

from larek.apps.product_seller.models import ProductSeller


class ProductSellerFilter(FilterSet):
    in_stock = rest_framework.CharFilter(method="filter_in_stock")

    def filter_in_stock(self, queryset, name, value):
        return queryset.filter(products_count__gt=0) if value == "on" else queryset

    class Meta:
        model = ProductSeller
        fields = {
            "price": ["gte", "lte"],
            "product__name": ["icontains"],
            "product__catalog_category__id": ["exact"],
        }
