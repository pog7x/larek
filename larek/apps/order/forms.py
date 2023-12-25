from django import forms

from larek.apps.order.models import Order


class OrderCreateForm(forms.ModelForm):
    user_id = forms.IntegerField(required=False)
    full_name = forms.CharField()
    phone = forms.CharField()
    address = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Order
        fields = [
            "full_name",
            "phone",
            "email",
            "address",
            "user_id",
        ]
