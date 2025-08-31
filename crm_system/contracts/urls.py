from django.urls import path

from contracts.views import (
    ContractsListView,
    ContractsCreateView,
    ContractsDetailView,
    ContractsUpdateView,
    ContractsDeleteView,
)


app_name = "contracts"

urlpatterns = [
    path("new/", ContractsCreateView.as_view(), name="contract_create"),
    path("<int:pk>/", ContractsDetailView.as_view(), name="contract_details"),
    path("<int:pk>/edit/", ContractsUpdateView.as_view(), name="contract_edit"),
    path("<int:pk>/delete/", ContractsDeleteView.as_view(), name="contract_delete"),
    path("", ContractsListView.as_view(), name="contracts_list"),
]
