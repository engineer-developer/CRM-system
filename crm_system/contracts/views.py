from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect

from contracts.forms import ContractForm
from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead


class ContractsListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка контрактов"""

    permission_required = ["contracts.view_contract"]
    model = Contract
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    ordering = ["created_at"]


class ContractsCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания нового контракта"""

    permission_required = ["contracts.add_contract"]
    model = Contract
    template_name = "contracts/contracts-create.html"
    form_class = ContractForm
    success_url = reverse_lazy("contracts:contracts_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.get_form_class())
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        contract: Contract = form.save(commit=False)

        product = form.cleaned_data.get("product")
        contract.name = f"Контракт об оказании услуги '{product.name}'"
        contract.cost = product.cost

        lead: Lead = form.cleaned_data.get("lead")
        customer, _ = Customer.objects.get_or_create(lead=lead)
        contract.customer = customer

        contract.save()
        return HttpResponseRedirect(reverse("contracts:contracts_list"))


class ContractsDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации о контракте"""

    permission_required = ["contracts.view_contract"]
    model = Contract
    template_name = "contracts/contracts-detail.html"


class ContractsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для обновления информации о контракте"""

    permission_required = ["contracts.change_contract"]
    model = Contract
    template_name = "contracts/contracts-edit.html"
    form_class = ContractForm

    def post(self, request, *args, pk=None, **kwargs):

        form = self.get_form(self.get_form_class())
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        contract: Contract = Contract.objects.get(pk=pk)
        cleaned_data = form.cleaned_data
        for key, value in cleaned_data.items():
            setattr(contract, key, value)

        product = cleaned_data.get("product")
        contract.name = f"Контракт об оказании услуги '{product.name}'"

        contract.cost = product.cost

        lead: Lead = cleaned_data.get("lead")
        customer, _ = Customer.objects.get_or_create(lead=lead)
        contract.customer = customer

        contract.save()
        return HttpResponseRedirect(
            reverse(
                "contracts:contract_details",
                kwargs={"pk": contract.pk},
            )
        )


class ContractsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления контракта"""

    permission_required = ["contracts.delete_contract"]
    model = Contract
    template_name = "contracts/contracts-delete.html"
    success_url = reverse_lazy("contracts:contracts_list")

    def form_valid(self, form):
        """
        Удаляя контракты, проверяем есть ли у клиента другие контракты.
        Если у клиента контрактов нет,
        убираем его из активных клиентов (удаляем клиента без контрактов)
        """

        contract: Contract = self.object
        customer: Customer = contract.customer

        contract.delete()

        if not customer.contracts.exists():
            customer.delete()

        return HttpResponseRedirect(self.get_success_url())
