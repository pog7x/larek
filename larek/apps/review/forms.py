from django import forms

from larek.apps.review.models import Review


class CreateReviewForm(forms.ModelForm):
    comment = forms.CharField(required=True)
    product_id = forms.IntegerField(required=True)
    user_id = forms.IntegerField(required=True)

    class Meta:
        model = Review
        fields = ("comment", "user_id", "product_id")

    def save(self, commit=True):
        if self.errors:
            raise ValueError(
                "The {} could not be {} because the data didn't validate.".format(
                    self.instance._meta.object_name,
                    "created" if self.instance._state.adding else "changed",
                )
            )
        if commit:
            self.instance = self._meta.model(**self.cleaned_data)
            self.instance.save()

        return self.instance
