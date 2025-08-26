from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexPageView(LoginRequiredMixin, TemplateView):
    """Представление исходной страницы приложения"""

    template_name = "crm_app/index.html"
