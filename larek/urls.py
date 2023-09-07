from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework import routers

from larek.apps.cart.views import CartViewSet
from larek.apps.catalog_category.views import CatalogCategoryViewSet
from larek.apps.order.views import OrderViewSet
from larek.apps.payment.views import PaymentViewSet
from larek.apps.product.views import ProductViewSet
from larek.apps.product_seller.views import ProductSellerViewSet
from larek.apps.review.views import ReviewViewSet
from larek.apps.role.views import RoleViewSet
from larek.apps.seller.views import SellerViewSet
from larek.apps.user.views import (
    UserLoginView,
    UserLogoutView,
    UserRegistrationView,
    UserViewSet,
)
from larek.apps.views_history.views import ViewsHistoryViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"cart", CartViewSet)
router.register(r"catalog_category", CatalogCategoryViewSet)
router.register(r"order", OrderViewSet)
router.register(r"payment", PaymentViewSet)
router.register(r"product", ProductViewSet)
router.register(r"product_seller", ProductSellerViewSet)
router.register(r"review", ReviewViewSet)
router.register(r"role", RoleViewSet)
router.register(r"seller", SellerViewSet)
router.register(r"user", UserViewSet)
router.register(r"views_history", ViewsHistoryViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include((router.urls))),
    path(
        "catalog/",
        TemplateView.as_view(template_name="catalog.html"),
        name="catalog",
    ),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("", TemplateView.as_view(template_name="index.html"), name="index"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path(
        "registration/",
        UserRegistrationView.as_view(template_name="registration.html"),
        name="registration",
    ),
    path(
        "product/<int:product_id>/",
        TemplateView.as_view(template_name="product.html"),
        name="product",
    ),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
