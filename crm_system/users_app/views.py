from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from users_app.forms import UserCreateForm, UserUpdateForm


class UsersListView(ListView):
    """Представление списка пользователей"""

    model = User
    template_name = "users_app/users-list.html"
    queryset = User.objects.filter(is_superuser=False).filter(is_active=True)
    context_object_name = "users"


class UserDetailView(DetailView):
    """Представление информации о пользователе"""

    model = User
    template_name = "users_app/users-detail.html"


class UserCreateView(CreateView):
    """Представление для создания пользователя"""

    model = User
    template_name = "users_app/users-create.html"
    form_class = UserCreateForm


class UserUpdateView(UpdateView):
    """Представление для редактирования пользователя"""

    model = User
    template_name = "users_app/users-edit.html"
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse(
            "users_app:user_details",
            kwargs={"pk": self.object.pk},
        )
