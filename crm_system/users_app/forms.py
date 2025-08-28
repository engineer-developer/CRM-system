from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from django import forms


class UserCreateForm(forms.ModelForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        initial="1",
        widget=forms.RadioSelect(),
        label="Роль пользователя в системе",
        help_text="",
    )

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


class UserUpdateForm(ModelForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        initial="администратор",
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Изменить роль пользователя",
        help_text="",
    )

    class Meta:
        model = User
        fields = ("last_name", "first_name", "email", "groups")
        widgets = {
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group = self.instance.groups.all()[0]
        print(f"group: {group.name}")
        self.fields["groups"].initial = group.pk

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Удаляем все группы и добавляем выбранную
            user.groups.clear()
            groups = self.cleaned_data["groups"]
            print(f"cleaned_data: {groups}")
            user.groups.add(self.cleaned_data["groups"])
        return user
