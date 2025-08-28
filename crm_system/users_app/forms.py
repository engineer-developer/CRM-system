from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "last_name", "first_name", "email", "groups")

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "login"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control", "placeholder": "password"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "фамилия"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "имя"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "example@email.com"}
            ),
            "groups": forms.Select,
        }
        help_texts = {
            "groups": "",
        }
        labels = {
            "username": "Login пользователя",
            "groups": "Роль пользователя в системе",
        }


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ("last_name", "first_name", "email", "groups")
        widgets = {
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "groups": forms.RadioSelect(),
        }
        help_texts = {
            "groups": "",
        }
        labels = {
            "groups": "Изменить роль пользователя",
        }
