from django.test import TestCase
from django.urls import reverse

from crm_core.tests import TestClientMixin


class UsersTests(TestClientMixin, TestCase):
    """Тесты для пользователей"""

    def test_can_get_all_users(self):
        """Тест возможности получить список всех пользователей"""
        url = reverse("users:users_list")

        response = self.test_client.get(url)
        self.assertEqual(response.status_code, 200, "status code is not 200")

        users = response.context["users"]
        self.assertTrue(users.count() > 0, "users not found")
