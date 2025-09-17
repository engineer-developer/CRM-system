from django.urls import path

from products.views import (
    ProductsListView,
    ProductsCreateView,
    ProductsDetailView,
    ProductsUpdateView,
    ProductsDeleteView,
)


app_name = "products"

urlpatterns = [
    path("new/", ProductsCreateView.as_view(), name="product_create"),
    path("<int:pk>/", ProductsDetailView.as_view(), name="product_details"),
    path("<int:pk>/edit/", ProductsUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductsDeleteView.as_view(), name="product_delete"),
    path("", ProductsListView.as_view(), name="products_list"),
]
