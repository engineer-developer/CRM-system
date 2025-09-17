import datetime

from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect

from contracts.forms import ContractForm
from contracts.models import Contract
from contracts.utils import contract_name_factory
from customers.models import Customer
from leads.models import Lead


class ContractsListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка контрактов"""

    permission_required = ["contracts.view_contract"]
    model = Contract
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"
    ordering = ["-created_at"]

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class ContractsCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания нового контракта"""

    permission_required = ["contracts.add_contract"]
    model = Contract
    template_name = "contracts/contracts-create.html"
    form_class = ContractForm
    success_url = reverse_lazy("contracts:contracts_list")

    def post(self, request, *args, **kwargs):
        form = ContractForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form}, status=400)

        contract = form.save(commit=False)

        lead: Lead = form.cleaned_data.get("lead")
        customer, _ = Customer.objects.get_or_create(lead=lead)
        if not customer.is_active:
            customer.is_active = True
            customer.save()

        contract.customer = customer
        contract.cost = contract.product.cost
        contract.name = contract_name_factory(contract)
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

    def get_success_url(self):
        obj = self.object
        return reverse(
            "contracts:contract_details",
            kwargs={"pk": obj.pk},
        )

    def get_initial(self, *args, **kwargs):
        """Предзаполняем поля формы"""
        initial = super().get_initial()
        contract: Contract = self.object

        initial["lead"] = contract.customer.lead
        initial["start_date"] = datetime.datetime.strftime(
            contract.start_date, "%Y-%m-%d"
        )
        initial["end_date"] = datetime.datetime.strftime(contract.end_date, "%Y-%m-%d")
        return initial

    def post(self, request, *args, pk=None, **kwargs):
        """Обновляем сведения о контракте"""
        contract = Contract.objects.get(pk=pk)
        form = ContractForm(request.POST, request.FILES, instance=contract)
        context = {
            "form": form,
            "object": contract,
        }
        if not form.is_valid():
            return render(request, self.template_name, context)

        contract = form.save(commit=False)

        lead = form.cleaned_data.get("lead")
        customer, _ = Customer.objects.get_or_create(lead=lead)
        contract.customer = customer

        contract.cost = contract.product.cost
        contract.name = contract_name_factory(contract)
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
