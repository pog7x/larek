import logging

from django import forms

from larek.apps.cart.models import Cart

log = logging.getLogger(__name__)


class CartCreateForm(forms.ModelForm):
    product_seller_id = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)
    products_count = forms.IntegerField(required=True)

    class Meta:
        model = Cart
        fields = ("product_seller_id", "user_id", "products_count")


class CartUpdateForm(forms.ModelForm):
    products_count = forms.IntegerField(required=True)

    class Meta:
        model = Cart
        fields = ("products_count",)
