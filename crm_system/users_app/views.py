from django.contrib.auth.models import User
from django.shortcuts import render
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import (
    View,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from users_app.forms import UserCreateForm, UserUpdateForm, UserPasswordForm


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

class UserPasswordUpdateView(View):
    """Представление для изменения пароля пользователя"""

    template_name = "users_app/users-password-update.html"

    def get(self, request, *args, pk=None, **kwargs):
        """Рендеринг формы изменения пароля пользователя"""
        user = get_object_or_404(User, pk=pk)
        form = UserPasswordForm()
        context = {
            "object": user,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, pk=None, **kwargs):
        """Обработка данных переданных в форму изменения пароля пользователя"""
        user = User.objects.get(pk=pk)
        form = UserPasswordForm(request.POST)

        if not form.is_valid():
            context = {"object": user, "form": form}
            return render(request, self.template_name, context)

        password = form.cleaned_data["password1"]
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(
            reverse(
                "users_app:user_details",
                kwargs={"pk": user.pk},
            )
        )
