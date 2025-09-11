from django.test import TestCase
from django.urls import reverse

from crm_core.tests import TestClientMixin


class ProductsTests(TestClientMixin, TestCase):
    """Тесты для услуг"""

    def test_can_get_all_products(self):
        """Тест возможности получить список всех услуг"""
        url = reverse("products:products_list")

        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")

        products = response.context["products"]
        self.assertTrue(products.count() > 0, "products not found")
