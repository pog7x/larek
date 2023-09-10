from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    BaseUserCreationForm,
    UsernameField,
)

from larek.apps.user.models import User


class UserRegistrationForm(BaseUserCreationForm):
    username = UsernameField(
        label=False,
        widget=forms.TextInput(
            attrs={
                "class": "user-input",
                "id": "username",
                "type": "text",
                "placeholder": "Username",
            },
        ),
    )
    email = forms.EmailField(
        label=False,
        widget=forms.EmailInput(
            attrs={
                "class": "user-input",
                "type": "email",
                "id": "email",
                "placeholder": "Email",
            },
        ),
    )
    password1 = forms.CharField(
        label=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "password1",
                "placeholder": "Password",
                "autocomplete": "new-password",
            },
        ),
    )
    password2 = forms.CharField(
        label=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "type": "password",
                "id": "password2",
                "placeholder": "Password confirmation",
                "autocomplete": "new-password",
            },
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = UsernameField(
        label=False,
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                "class": "user-input",
                "type": "text",
                "placeholder": "Username",
                "id": "username",
            }
        ),
    )
    password = forms.CharField(
        label=False,
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "type": "password",
                "id": "password",
                "placeholder": "*********",
            }
        ),
    )


class ClearableFileInputForAvatar(forms.ClearableFileInput):
    template_name = "user/clearablefileinputforavatar.html"
    input_text = "Change avatar"
    clear_checkbox_label = "Clear avatar"


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)

    def save(self, commit=True):
        self.instance.avatar = self.instance.avatar or "user/default_avatar.svg"
        return super().save(commit=commit)

    class Meta:
        model = User
        fields = ("avatar", "first_name", "last_name", "phone", "email")
        widgets = {
            "avatar": ClearableFileInputForAvatar,
        }
