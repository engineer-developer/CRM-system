from django.test import TestCase
from django.urls import reverse

from crm_core.tests import TestClientMixin


class AdsTests(TestClientMixin, TestCase):
    """Тесты для рекламных кампаний"""

    def test_can_get_all_ads(self):
        """Тест возможности получить список всех рекламных кампаний"""
        url = reverse("ads:ads_list")

        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")

        ads = response.context["ads"]
        self.assertTrue(ads.count() > 0, "ads not found")
