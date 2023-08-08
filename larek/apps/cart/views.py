import logging

from django.shortcuts import HttpResponse, redirect, render
from django.views import View

from larek.apps.cart.models import Cart
from larek.apps.product_seller.models import ProductSeller

logger = logging.getLogger(__name__)


class CartView(View):
    def get(self, request):
        cart = Cart.objects.prefetch_related("product_seller").all()
        return render(
            request,
            "cart.html",
            {
                "cart": cart,
                "total": sum(c.products_count * c.product_seller.price for c in cart),
            },
        )


class CartDeleteView(View):
    def get(self, _, cart_id):
        Cart.objects.filter(id=cart_id).delete()
        return redirect("cart")


class CartProductsCountView(View):
    def get(self, request, cart_id):
        products_count: str = request.GET.get("products_count")
        product_seller: str = request.GET.get("product_seller")

        to_update = {}
        try:
            products_count_int = int(products_count) if products_count else None
            if products_count_int and products_count_int > 0:
                to_update["products_count"] = products_count_int
            if product_seller:
                ps = ProductSeller.objects.get(id=product_seller)
                to_update["product_seller"] = ps
        except:
            pass

        logger.info(f"{to_update} <<<<<<<")
        Cart.objects.filter(id=cart_id).update(
            **to_update,
        )

        cart = Cart.objects.prefetch_related("product_seller").all()

        return HttpResponse(
            sum(c.products_count * c.product_seller.price for c in cart)
        )
