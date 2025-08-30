from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

from products_app.forms import ProductForm
from products_app.models import Product


class ProductsListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка услуг"""

    permission_required = ["products_app.view_product"]
    model = Product
    template_name = "products_app/products-list.html"
    context_object_name = "products"
    ordering = ["name"]


class ProductsCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания новой услуги"""

    permission_required = ["products_app.add_product"]
    model = Product
    template_name = "products_app/products-create.html"
    form_class = ProductForm
    success_url = reverse_lazy("products_app:products_list")


class ProductsDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации об услуге"""

    permission_required = ["products_app.view_product"]
    model = Product
    template_name = "products_app/products-detail.html"


class ProductsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для обновления информации об услуге"""

    permission_required = ["products_app.change_product"]
    model = Product
    template_name = "products_app/products-edit.html"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "products_app:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления услуги"""

    permission_required = ["products_app.delete_product"]
    model = Product
    template_name = "products_app/products-delete.html"
    success_url = reverse_lazy("products_app:products_list")
