from django import forms

from larek.apps.payment.models import Payment


class PaymentProcessForm(forms.ModelForm):
    card_number = forms.CharField(required=True)

    class Meta:
        model = Payment
        fields = ("card_number", "status")
