from django.urls import path

from users_app.views import (
    UsersListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserPasswordUpdateView,
    UserDeleteView,
)


app_name = "users"

urlpatterns = [
    path("new/", UserCreateView.as_view(), name="user_create"),
    path("<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path(
        "<int:pk>/pass/change/",
        UserPasswordUpdateView.as_view(),
        name="user_change_pass",
    ),
    path("<int:pk>/", UserDetailView.as_view(), name="user_details"),
    path("", UsersListView.as_view(), name="users_list"),
]
