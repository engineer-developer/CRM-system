from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from django import forms


class UserCreateForm(forms.ModelForm):
    """Форма для создания пользователя"""

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
        }
        labels = {
            "username": "Login пользователя",
        }

    some = forms.RadioSelect()

    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        initial=1,
        widget=forms.RadioSelect(),
        label="Роль пользователя в системе",
        help_text="",
    )


class UserUpdateForm(ModelForm):
    """Форма для обновления пользователя"""

    class Meta:
        model = User
        fields = ("last_name", "first_name", "email", "groups")
        widgets = {
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        initial=1,
        required=True,
        widget=forms.RadioSelect(),
        label="Изменить роль пользователя",
        help_text="",
    )

    def save(self, commit=True):
        """Сохраняем пользователя с обновленным значением groups"""
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.clear()
            groups = self.cleaned_data["groups"]
            user.groups.add(groups)
        return user
