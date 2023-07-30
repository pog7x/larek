import logging

from django.shortcuts import render
from django.views import View
from larek.apps.product.forms import CatalogFilterForm
from larek.apps.product.models import Product
from larek.apps.product_seller.models import ProductSeller

logger = logging.getLogger(__name__)


async def index(request):
    return render(request, "index.html", {})


async def about(request):
    return render(request, "about.html", {})


async def sale(request):
    return render(request, "sale.html", {})


async def comparison(request):
    return render(request, "comparison.html", {})


async def oneorder(request):
    return render(request, "oneorder.html", {})


async def order(request):
    return render(request, "order.html", {})


async def payment(request):
    return render(request, "payment.html", {})


async def progresspayment(request):
    return render(request, "progresspayment.html", {})


async def paymentsomeone(request):
    return render(request, "paymentsomeone.html", {})


class ProductDetailView(View):
    def get(self, request, product_id):
        product_seller = ProductSeller.objects.select_related(
            "product",
        ).get(
            id=product_id,
        )

        return render(request, "product.html", {"product_seller": product_seller})


class CatalogView(View):
    def get(self, request):
        catalog_form = CatalogFilterForm(request.GET)
        if not request.GET:
            product_seller = ProductSeller.objects.select_related("product").all()
        else:
            price = request.GET.get("price")
            price_gte, price_lte = price.split(";") if price else (None, None)
            name_like = request.GET.get("name_like")
            in_stock = request.GET.get("in_stock")
            free_delivery = request.GET.get("free_delivery")

            to_filter = {}

            if price_gte:
                to_filter["price__gte"] = price_gte
            if price_gte:
                to_filter["price__lte"] = price_lte
            if name_like:
                to_filter["product__name__icontains"] = name_like
            if in_stock:
                to_filter["products_count__gt"] = 0

            product_seller = ProductSeller.objects.select_related(
                "product",
            ).filter(
                **to_filter,
            )

        return render(
            request,
            "catalog.html",
            {
                "catalog_form": catalog_form,
                "product_seller": product_seller,
            },
        )
