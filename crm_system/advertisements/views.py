import datetime
from decimal import Decimal

from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.functions import Coalesce, Round
from django.urls import reverse_lazy
from django.views import generic
from django.db.models import (
    Q,
    Count,
    Subquery,
    OuterRef,
    Sum,
    DecimalField,
    Case,
    When,
    F,
)

from advertisements.forms import AdvertisementForm
from advertisements.models import Advertisement


class AdsListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка рекламных кампаний"""

    permission_required = ["advertisements.view_advertisement"]
    model = Advertisement
    template_name = "advertisements/ads-list.html"
    context_object_name = "ads"
    ordering = ["created_at"]


class AdsCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания рекламной кампании"""

    permission_required = ["advertisements.add_advertisement"]
    model = Advertisement
    template_name = "advertisements/ads-create.html"
    form_class = AdvertisementForm
    success_url = reverse_lazy("ads:ads_list")


class AdsDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации о рекламной кампании"""

    permission_required = ["advertisements.view_advertisement"]
    model = Advertisement
    template_name = "advertisements/ads-detail.html"


class AdsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление по обновлению информации о рекламной кампании"""

    permission_required = ["advertisements.change_advertisement"]
    model = Advertisement
    template_name = "advertisements/ads-edit.html"
    form_class = AdvertisementForm

    def get_success_url(self):
        return reverse_lazy("ads:ad_details", kwargs={"pk": self.object.pk})

    def get_initial(self):
        initial = super().get_initial()
        print(f"initial: {initial}")
        obj = self.object
        initial["start_date"] = datetime.datetime.strftime(obj.start_date, "%Y-%m-%d")
        initial["end_date"] = datetime.datetime.strftime(obj.end_date, "%Y-%m-%d")
        return initial


class AdsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления рекламной кампании"""

    permission_required = ["advertisements.delete_advertisement"]
    model = Advertisement
    template_name = "advertisements/ads-delete.html"
    success_url = reverse_lazy("ads:ads_list")


class AdsStatisticListView(PermissionRequiredMixin, generic.ListView):
    """Представление для просмотра статистики по рекламным кампаниям"""

    permission_required = ["advertisements.view_advertisement"]
    model = Advertisement
    template_name = "advertisements/ads-statistic.html"
    context_object_name = "ads"
    ordering = ["-product__cost"]

    def get_queryset(self):
        contract_model = apps.get_model("contracts", "Contract")

        total_contracts_cost_subquery = (
            contract_model.objects.filter(
                product__advertisements=OuterRef("pk"), is_active=True
            )
            .values("product__advertisements")
            .annotate(total_cost=Sum("cost"))
            .values("total_cost")[:1]
        )

        qs = super().get_queryset()
        qs = qs.annotate(
            leads_count=Count("leads", distinct=True),
            customers_count=Count(
                "product__contracts__customer",
                filter=Q(
                    product__contracts__is_active=True,
                    product__contracts__customer__is_active=True,
                ),
                distinct=True,
            ),
            total_contracts_cost=Coalesce(
                Subquery(
                    total_contracts_cost_subquery,
                    output_field=DecimalField(max_digits=10, decimal_places=2),
                ),
                Decimal(0.0),
            ),
            # Вычисляем profit: total_contracts_cost / budget, с защитой от деления на 0
            profit=Case(
                When(
                    budget__gt=0, then=Round(F("total_contracts_cost") / F("budget"), 2)
                ),
                default=Decimal(0.0),
                output_field=DecimalField(max_digits=10, decimal_places=2),
            ),
        )
        return qs
