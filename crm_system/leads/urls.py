from django.urls import path


from leads.views import (
    LeadsCreateView,
    LeadsDetailView,
    LeadsUpdateView,
    LeadsDeleteView,
    LeadsListView,
)

app_name = "leads"

urlpatterns = [
    path("new/", LeadsCreateView.as_view(), name="lead_create"),
    path("<int:pk>/", LeadsDetailView.as_view(), name="lead_details"),
    path("<int:pk>/edit/", LeadsUpdateView.as_view(), name="lead_edit"),
    path("<int:pk>/delete/", LeadsDeleteView.as_view(), name="lead_delete"),
    path("", LeadsListView.as_view(), name="leads_list"),
]
