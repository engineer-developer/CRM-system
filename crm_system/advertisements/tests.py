from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class AdsTests(TestCase):
    """Тесты для рекламных кампаний"""

    fixtures = ("db_data_full.json",)

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        user = User.objects.get(username="admin")
        self.test_client = Client()
        self.test_client.force_login(user)

    def test_can_get_all_ads(self):
        url = reverse("ads:ads_list")
        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")
        ads = response.context["ads"]
        self.assertTrue(ads.count() > 0, "ads not found")
