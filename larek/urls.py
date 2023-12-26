from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve
from rest_framework import routers

from larek.apps.banner.views import BannerProductSellerListView
from larek.apps.cart.views import (
    CartCreateView,
    CartItemView,
    CartListView,
    CartTotalHeaderView,
    CartTotalListView,
    CartTotalView,
    CartViewSet,
)
from larek.apps.catalog_category.views import CatalogCategoryViewSet
from larek.apps.delivery.views import DeliveryViewSet
from larek.apps.order.views import (
    OrderCreateView,
    OrderDetailView,
    OrdersHistoryView,
    OrderViewSet,
)
from larek.apps.payment.views import PaymentProcessView, PaymentViewSet, PaymentWaitView
from larek.apps.product.views import ProductViewSet
from larek.apps.product_seller.views import (
    ProductSellerDetailView,
    ProductSellerListView,
    ProductSellerViewSet,
)
from larek.apps.review.views import ReviewCreateView, ReviewViewSet
from larek.apps.role.views import RoleViewSet
from larek.apps.seller.views import SellerViewSet
from larek.apps.user.views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserProfileView,
    UserRegistrationView,
    UserViewSet,
)
from larek.apps.views_history.views import ViewsHistoryViewSet

router = routers.SimpleRouter(trailing_slash=False)

router.register(r"cart", CartViewSet)
router.register(r"catalog_category", CatalogCategoryViewSet)
router.register(r"delivery", DeliveryViewSet)
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
    # API
    path("api/", include(router.urls)),
    path("api/cart_total", CartTotalView.as_view()),
    # Home page
    path("", BannerProductSellerListView.as_view(), name="index"),
    # Catalog
    path("catalog/", ProductSellerListView.as_view(), name="catalog"),
    # About
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    # Cart
    path("cart_change/", CartCreateView.as_view(), name="cart_change"),
    path("cart/<int:pk>/", CartItemView.as_view(), name="cart_item"),
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart_total_header/", CartTotalHeaderView.as_view(), name="cart_total_header"),
    path("cart_total_list/", CartTotalListView.as_view(), name="cart_total_list"),
    # Profile
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path(
        "registration/",
        UserRegistrationView.as_view(template_name="registration.html"),
        name="registration",
    ),
    path("password_change/", UserPasswordChangeView.as_view(), name="password_change"),
    path(
        "password_reset/",
        PasswordResetView.as_view(template_name="password_reset_1.html"),
        name="password_reset",
    ),
    re_path(
        r"^password_reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmView.as_view(template_name="password_reset_2.html"),
        name="password_reset_confirm",
    ),
    path(
        "password_reset_done/",
        PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password_reset_complete/",
        PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
        name="password_reset_complete",
    ),
    # Product detail
    path(
        "product_seller/<int:pk>/",
        ProductSellerDetailView.as_view(),
        name="product_seller",
    ),
    # Order
    path("order/", OrderCreateView.as_view(), name="order"),
    path("orders_history/", OrdersHistoryView.as_view(), name="orders_history"),
    path("oneorder/<int:pk>", OrderDetailView.as_view(), name="oneorder"),
    # Payment
    path("payment/<uuid:pk>/", PaymentProcessView.as_view(), name="payment"),
    path(
        "progresspayment/<uuid:pk>/", PaymentWaitView.as_view(), name="progresspayment"
    ),
    # Review
    path("review/", ReviewCreateView.as_view(), name="review_create"),
    # Mediafiles
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
