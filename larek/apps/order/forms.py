from django import forms

from larek.apps.order.models import Order


class OrderCreateForm(forms.ModelForm):
    full_name = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()
    user_id = forms.IntegerField()
    delivery_id = forms.IntegerField()

    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "email", "user_id", "delivery_id"]
