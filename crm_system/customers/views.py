from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

from contracts.models import Contract
from customers.forms import (
    CustomerCreateForm,
    CustomerUpdateForm,
    CustomerCreateFromLeadForm,
)
from customers.models import Customer
from contracts.utils import create_contract
from leads.models import Lead
from products.models import Product


class CustomersListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка клиентов"""

    permission_required = ["customers.view_customer"]
    queryset = Customer
    template_name = "customers/customers-list.html"
    context_object_name = "customers"

    def get_queryset(self):
        return Customer.objects.filter(is_active=True).select_related("lead")


class CustomerCreateFromLeadView(PermissionRequiredMixin, generic.FormView):
    """Представление для создания клиента на основе лида"""

    permission_required = ["customers.add_customer"]
    template_name = "customers/customers-create_from_lead.html"

    def get(self, request, *args, pk=None, **kwargs):
        form = CustomerCreateFromLeadForm()
        context = {"form": form, "lead_pk": pk}
        return render(request, self.template_name, context)

    def post(self, request, *args, pk=None, **kwargs):
        form = CustomerCreateFromLeadForm(request.POST)
        if not form.is_valid():
            context = {"form": form, "lead_pk": pk}
            return render(request, self.template_name, context, status=400)

        cleaned_data = form.cleaned_data
        lead: Lead = Lead.objects.get(pk=pk)
        customer, _ = Customer.objects.get_or_create(lead=lead)
        product: Product = cleaned_data.get("product")
        contract = create_contract(
            product=product,
            customer=customer,
            start_date=cleaned_data.get("start_date"),
            end_date=cleaned_data.get("end_date"),
        )
        if not contract:
            return HttpResponse("Failed to create contract", status=400)
        return HttpResponseRedirect(reverse("customers:customers_list"))


class CustomersCreateView(CustomerCreateFromLeadView):
    """Представление для создания клиента"""

    template_name = "customers/customers-create.html"

    def get(self, request, *args, **kwargs):
        """Передаем форму для заполнения исходными данными"""
        form = CustomerCreateForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        """Создаем клиента на основе данных формы"""
        form = CustomerCreateForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form}, status=400)

        cleaned_data = form.cleaned_data
        lead: Lead = cleaned_data.get("lead")
        product: Product = form.cleaned_data.get("product")
        customer, _ = Customer.objects.get_or_create(lead=lead)
        if not customer.is_active:
            customer.is_active = True
            customer.save()
        contract = create_contract(
            product=product,
            customer=customer,
            start_date=cleaned_data.get("start_date"),
            end_date=cleaned_data.get("end_date"),
        )
        if not contract:
            return HttpResponse("Failed to create contract", status=400)
        return HttpResponseRedirect(reverse("customers:customers_list"))


class CustomersDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации о клиенте"""

    permission_required = ["customers.view_customer"]
    model = Customer
    template_name = "customers/customers-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(
            contracts__customer=self.object,
            contracts__is_active=True,
        )
        context["products"] = products
        return context


class CustomersUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для обновления информации о клиенте"""

    permission_required = ["customers.change_customer"]
    model = Customer
    template_name = "customers/customers-edit.html"
    form_class = CustomerUpdateForm
    context_object_name = "object"

    def get_success_url(self):
        return reverse(
            "customers:customer_details",
            kwargs={"pk": self.object.pk},
        )

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial()
        customer = self.object
        lead = customer.lead
        initial["last_name"] = lead.last_name
        initial["first_name"] = lead.first_name
        initial["phone"] = lead.phone
        initial["email"] = lead.email
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contracts = Contract.objects.filter(
            customer=self.object,
            is_active=True,
        ).prefetch_related("product")
        context["contracts"] = contracts
        return context

    def post(self, request, *args, **kwargs):
        customer: Customer = self.object
        form = CustomerUpdateForm(request.POST, instance=customer)
        context = {"form": form, "object": customer}
        if not form.is_valid():
            return render(request, self.template_name, context, status=400)

        cleaned_data = form.cleaned_data
        lead: Lead = customer.lead
        lead.last_name = cleaned_data.get("last_name")
        lead.first_name = cleaned_data.get("first_name")
        lead.phone = cleaned_data.get("phone")
        lead.email = cleaned_data.get("email")
        lead.save()
        return HttpResponseRedirect(
            reverse(
                "customers:customer_details",
                kwargs={"pk": customer.pk},
            )
        )


class CustomersDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления клиента"""

    permission_required = ["customers.delete_customer"]
    model = Customer
    template_name = "customers/customers-delete.html"
    success_url = reverse_lazy("customers:customers_list")


class CustomersContractDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления контракта клиента"""

    permission_required = ["customers.delete_customer"]
    model = Contract
    template_name = "customers/customers-contract-delete.html"

    def get_success_url(self):
        return reverse(
            "customers:customer_details",
            kwargs={"pk": self.object.customer.pk},
        )
