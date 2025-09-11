from django.test import Client
from django.contrib.auth import get_user_model


User = get_user_model()


class TestClientMixin:
    fixtures = ("db_data_full.json",)

    @classmethod
    def setUpClass(self):
        super().setUpClass()
        user = User.objects.get(username="admin")
        self.test_client = Client()
        self.test_client.force_login(user)
