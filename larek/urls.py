"""
URL configuration for larek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from larek.apps.cart.views import CartDeleteView, CartProductsCountView, CartView
from larek.apps.pepe.views import pepe, pepe1
from larek.apps.product.views import (
    CatalogView,
    ProductDetailView,
    about,
    comparison,
    index,
    oneorder,
    order,
    payment,
    paymentsomeone,
    progresspayment,
    sale,
)
from larek.apps.user.views import (
    account,
    email,
    historyorder,
    login,
    password,
    profile,
    registration,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("pepe/", pepe),
    path("pepe_1/", pepe1),
    # cart
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/<int:cart_id>/", CartDeleteView.as_view(), name="delete_cart"),
    path(
        "cart/<int:cart_id>/products_count/",
        CartProductsCountView.as_view(),
        name="cart_products_count",
    ),
    # user
    path("registration/", registration, name="registration"),
    path("login/", login, name="login"),
    path("email/", email, name="email"),
    path("password/", password, name="password"),
    path("account/", account, name="account"),
    path("profile/", profile, name="profile"),
    path("historyorder/", historyorder, name="historyorder"),
    # product
    path("", index, name="index"),
    path("about/", about, name="about"),
    path("sale/", sale, name="sale"),
    path("catalog/", CatalogView.as_view(), name="catalog"),
    path("comparison/", comparison, name="comparison"),
    path("oneorder/", oneorder, name="oneorder"),
    path("order/", order, name="order"),
    path("payment/", payment, name="payment"),
    path("paymentsomeone/", paymentsomeone, name="paymentsomeone"),
    path("progresspayment/", progresspayment, name="progresspayment"),
    path("product/<int:product_id>/", ProductDetailView.as_view(), name="product"),
]
