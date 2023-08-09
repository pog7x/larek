from django_filters import rest_framework

from larek.apps.product_seller.models import ProductSeller


class ProductSellerFilter(rest_framework.FilterSet):
    in_stock = rest_framework.BooleanFilter(method="filter_in_stock")

    def filter_in_stock(self, queryset, name, value):
        return queryset.filter(products_count__lte=0) if value else queryset

    class Meta:
        model = ProductSeller
        fields = {
            "price": ["gte", "lte"],
            "product__name": ["icontains"],
        }
