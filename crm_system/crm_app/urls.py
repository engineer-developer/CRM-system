from django.urls import path

from crm_app.views import index_page


app_name = "crm_app"


urlpatterns = [
    path("", index_page, name="home_page"),
]
