from django.urls import path

from crm_app.views import IndexPageView


app_name = "crm_app"

urlpatterns = [
    path("", IndexPageView.as_view(), name="index_page"),
]
