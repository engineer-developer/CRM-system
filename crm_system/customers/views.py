from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

from customers.forms import CustomerForm
from customers.models import Customer


class CustomersListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка клиентов"""

    permission_required = ["customers.view_customer"]
    model = Customer
    template_name = "customers/customers-list.html"
    context_object_name = "customers"
    ordering = ["lead__last_name"]


class CustomersCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания клиента"""

    permission_required = ["customers.add_customer"]
    model = Customer
    template_name = "customers/customers-create.html"
    form_class = CustomerForm
    success_url = reverse_lazy("customers:customers_list")


class CustomersDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации о клиенте"""

    permission_required = ["customers.view_customer"]
    model = Customer
    template_name = "customers/customers-detail.html"


class CustomersUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для обновления информации о клиенте"""

    permission_required = ["customers.change_customer"]
    model = Customer
    template_name = "customers/customers-edit.html"
    form_class = CustomerForm

    def get_success_url(self):
        return reverse(
            "customers:customer_details",
            kwargs={"pk": self.object.pk},
        )


class CustomersDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления клиента"""

    permission_required = ["customers.delete_customer"]
    model = Customer
    template_name = "customers/customers-delete.html"
    success_url = reverse_lazy("customers:customers_list")
