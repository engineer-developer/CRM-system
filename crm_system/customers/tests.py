from django.test import TestCase
from django.urls import reverse

from crm_core.tests import TestClientMixin


class CustomersTests(TestClientMixin, TestCase):
    """Тесты для клиентов"""

    def test_can_get_all_customers(self):
        """Тест возможности получить список всех клиентов"""
        url = reverse("customers:customers_list")

        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")

        customers = response.context["customers"]
        self.assertTrue(customers.count() > 0, "customers not found")
