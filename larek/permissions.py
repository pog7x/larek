from rest_framework.permissions import BasePermission

from larek.apps.cart.models import Cart


class UserHasCartPermission(BasePermission):
    def has_permission(self, request, view):
        return Cart.user_has_carts(user_id=request.user.id)
