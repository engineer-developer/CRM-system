from django.urls import path

from auth_app.views import CustomLogoutView, CustomLoginView


app_name = "auth_app"


urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
]
