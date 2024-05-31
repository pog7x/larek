from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from larek.apps.banner.views import BannerListView
from larek.apps.cart.views import (
    CartCreateView,
    CartItemView,
    CartListView,
    CartTotalHeaderView,
    CartTotalListView,
)
from larek.apps.order.views import OrderCreateView, OrderDetailView, OrdersHistoryView
from larek.apps.payment.views import PaymentInitView, PaymentProgressView
from larek.apps.product_seller.views import (
    ProductSellerDetailView,
    ProductSellerListView,
)
from larek.apps.review.views import ReviewCreateView
from larek.apps.user.views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordChangeView,
    UserProfileView,
    UserRegistrationView,
)
from larek.apps.views_history.views import ViewsHistoryListView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Home page
    path("", BannerListView.as_view(), name="index"),
    # Catalog
    path("catalog/", ProductSellerListView.as_view(), name="catalog"),
    # About
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    # Cart
    path("cart/", CartListView.as_view(), name="cart"),
    path("cart/<int:pk>/", CartItemView.as_view(), name="cart_item"),
    path("cart_change/", CartCreateView.as_view(), name="cart_change"),
    path("cart_total_header/", CartTotalHeaderView.as_view(), name="cart_total_header"),
    path("cart_total_list/", CartTotalListView.as_view(), name="cart_total_list"),
    # Profile
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("registration/", UserRegistrationView.as_view(), name="registration"),
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
    # Product seller detail
    path(
        "product_seller/<int:pk>/",
        ProductSellerDetailView.as_view(),
        name="product_seller",
    ),
    # Order
    path("order/", OrderCreateView.as_view(), name="order"),
    path("order/<int:pk>", OrderDetailView.as_view(), name="order_item"),
    path("orders_history/", OrdersHistoryView.as_view(), name="orders_history"),
    # Payment
    path("payment/<uuid:pk>/", PaymentInitView.as_view(), name="payment"),
    path(
        "payment_progress/<uuid:pk>/",
        PaymentProgressView.as_view(),
        name="payment_progress",
    ),
    # Review
    path("review/", ReviewCreateView.as_view(), name="review_create"),
    # Views history
    path("views_history/", ViewsHistoryListView.as_view(), name="views_history"),
    # Mediafiles
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
