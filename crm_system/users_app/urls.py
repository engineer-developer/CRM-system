from django.urls import path

from users_app.views import (
    UsersListView,
    UserDetailView,
    UserCreateView,
    UserUpdateView,
    UserPasswordUpdateView,
    UserDeleteView,
)


app_name = "users_app"

urlpatterns = [
    path("users/new/", UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    path("users/<int:pk>/edit/", UserUpdateView.as_view(), name="user_edit"),
    path(
        "users/<int:pk>/pass/change/",
        UserPasswordUpdateView.as_view(),
        name="user_change_pass",
    ),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_details"),
    path("users/", UsersListView.as_view(), name="users_list"),
]
