from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

from products.forms import ProductForm
from products.models import Product


class ProductsListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка услуг"""

    permission_required = ["products.view_product"]
    model = Product
    template_name = "products/products-list.html"
    context_object_name = "products"
    ordering = ["name"]


class ProductsCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания новой услуги"""

    permission_required = ["products.add_product"]
    model = Product
    template_name = "products/products-create.html"
    form_class = ProductForm
    success_url = reverse_lazy("products:products_list")


class ProductsDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации об услуге"""

    permission_required = ["products.view_product"]
    model = Product
    template_name = "products/products-detail.html"


class ProductsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для обновления информации об услуге"""

    permission_required = ["products.change_product"]
    model = Product
    template_name = "products/products-edit.html"
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            "products:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления услуги"""

    permission_required = ["products.delete_product"]
    model = Product
    template_name = "products/products-delete.html"
    success_url = reverse_lazy("products:products_list")
