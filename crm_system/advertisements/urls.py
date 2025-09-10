from django.urls import path

from advertisements.views import (
    AdsListView,
    AdsCreateView,
    AdsDetailView,
    AdsUpdateView,
    AdsDeleteView,
    AdsStatisticListView,
)


app_name = "ads"

urlpatterns = [
    path("new/", AdsCreateView.as_view(), name="ad_create"),
    path("<int:pk>/", AdsDetailView.as_view(), name="ad_details"),
    path("<int:pk>/edit/", AdsUpdateView.as_view(), name="ad_edit"),
    path("<int:pk>/delete/", AdsDeleteView.as_view(), name="ad_delete"),
    path("statistic/", AdsStatisticListView.as_view(), name="ad_statistic"),
    path("", AdsListView.as_view(), name="ads_list"),
]
