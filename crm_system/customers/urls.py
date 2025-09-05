from django.urls import path


from customers.views import (
    CustomersCreateView,
    CustomersDetailView,
    CustomersUpdateView,
    CustomersDeleteView,
    CustomersListView,
    CustomerCreateFromLeadView,
)

app_name = "customers"

urlpatterns = [
    path(
        "new/lead/<int:pk>/",
        CustomerCreateFromLeadView.as_view(),
        name="customer_create_from_lead",
    ),
    path("new/", CustomersCreateView.as_view(), name="customer_create"),
    path("<int:pk>/", CustomersDetailView.as_view(), name="customer_details"),
    path("<int:pk>/edit/", CustomersUpdateView.as_view(), name="customer_edit"),
    path("<int:pk>/delete/", CustomersDeleteView.as_view(), name="customer_delete"),
    path("", CustomersListView.as_view(), name="customers_list"),
]
