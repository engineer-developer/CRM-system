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
    context_object_name = "users"
    ordering = ["last_name", "username"]

    def get_queryset(self) -> QuerySet[User]:
        """Получаем queryset пользователей"""
        qs = super().get_queryset()
        qs = (
            qs.filter(is_active=True)  # оставляем только активных пользователей
            .exclude(is_superuser=True)  # исключаем суперпользователей
            .exclude(id=self.request.user.pk)  # исключаем текущего пользователя
        )
        return qs


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
