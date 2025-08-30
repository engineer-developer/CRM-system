from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin

from leads.forms import LeadForm
from leads.models import Lead


class LeadsListView(PermissionRequiredMixin, generic.ListView):
    """Представление списка лидов"""

    permission_required = ["leads.view_lead"]
    model = Lead
    template_name = "leads/leads-list.html"
    context_object_name = "leads"
    ordering = ["last_name"]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(is_active=True)


class LeadsCreateView(PermissionRequiredMixin, generic.CreateView):
    """Представление для создания лида"""

    permission_required = ["leads.add_lead"]
    model = Lead
    template_name = "leads/leads-create.html"
    form_class = LeadForm
    success_url = reverse_lazy("leads:leads_list")


class LeadsDetailView(PermissionRequiredMixin, generic.DetailView):
    """Представление для просмотра подробной информации о лиде"""

    permission_required = ["leads.view_lead"]
    model = Lead
    template_name = "leads/leads-detail.html"


class LeadsUpdateView(PermissionRequiredMixin, generic.UpdateView):
    """Представление для обновления информации о лиде"""

    permission_required = ["leads.change_lead"]
    model = Lead
    template_name = "leads/leads-edit.html"
    form_class = LeadForm

    def get_success_url(self):
        return reverse(
            "leads:lead_details",
            kwargs={"pk": self.object.pk},
        )


class LeadsDeleteView(PermissionRequiredMixin, generic.DeleteView):
    """Представление для удаления лида"""

    permission_required = ["leads.delete_lead"]
    model = Lead
    template_name = "leads/leads-delete.html"
    success_url = reverse_lazy("leads:leads_list")
