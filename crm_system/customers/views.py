from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

from contracts.models import Contract
from customers.forms import CustomerForm
from customers.models import Customer
from leads.models import Lead
from products.models import Product


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

    def get(self, request, *args, **kwargs):
        """Передаем форму для заполнения исходными данными"""
        form = CustomerForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """Создаем клиента на основе данных формы"""
        form = CustomerForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form}, status=400)

        cleaned_data = form.cleaned_data
        lead: Lead = cleaned_data.get("lead")
        product: Product = form.cleaned_data.get("product")
        customer, _ = Customer.objects.get_or_create(lead=lead)
        contract: Contract = Contract(
            name=f"Контракт об оказании услуги '{product.name}'",
            cost=product.cost,
            product=product,
            lead=lead,
            customer=customer,
            start_date=cleaned_data.get("start_date"),
            end_date=cleaned_data.get("end_date"),
        )
        contract.save()
        return HttpResponseRedirect(reverse("customers:customers_list"))


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
    form_class = CustomerUpdateForm

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
