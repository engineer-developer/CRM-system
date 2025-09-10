from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from advertisements.models import Advertisement
from customers.models import Customer
from leads.models import Lead
from products.models import Product


class IndexPageView(LoginRequiredMixin, TemplateView):
    """Представление исходной страницы приложения"""

    template_name = "crm_app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["advertisements_count"] = Advertisement.objects.count()
        context["products_count"] = Product.objects.count()
        context["leads_count"] = Lead.objects.count()
        context["customers_count"] = Customer.objects.count()
        return context
