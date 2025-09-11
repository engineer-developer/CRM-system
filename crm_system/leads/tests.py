from django.test import TestCase
from django.urls import reverse

from crm_core.tests import TestClientMixin


class LeadsTests(TestClientMixin, TestCase):
    """Тесты для лидов"""

    def test_can_get_all_leads(self):
        """Тест возможности получить список всех лидов"""
        url = reverse("leads:leads_list")

        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")

        leads = response.context["leads"]
        self.assertTrue(leads.count() > 0, "leads not found")
