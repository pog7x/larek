from django import forms


class CatalogFilterForm(forms.Form):
    price = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "type": "text",
                "id": "price",
                "class": "range-line",
                "data-min": "0",
                "data-max": "99999",
                "data-type": "double",
            }
        ),
        required=False,
    )
    name_like = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-input form-input_full",
                "id": "title",
                "type": "text",
                "placeholder": "Название",
            },
        ),
        required=False,
    )
    in_stock = forms.BooleanField(required=False)
    free_delivery = forms.BooleanField(required=False)
