from django.test import TestCase
from django.urls import reverse

from crm_core.tests import TestClientMixin


class ContractsTests(TestClientMixin, TestCase):
    """Тесты для контрактов"""

    def test_can_get_all_contracts(self):
        """Тест возможности получить список всех контрактов"""
        url = reverse("contracts:contracts_list")

        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")

        contracts = response.context["contracts"]
        self.assertTrue(contracts.count() > 0, "contracts not found")
