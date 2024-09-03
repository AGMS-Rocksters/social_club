from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class LogoutAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@test.com"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )
        self.logout_url = reverse("logout")

    def test_logout(self):
        response = self.client.post(self.logout_url, {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logout_invalid(self):
        response = self.client.post(self.logout_url, {"refresh": "alkgflg8uz0p3qhgq"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_double_logout(self):
        response = self.client.post(self.logout_url, {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.post(self.logout_url, {"refresh": str(self.refresh)})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
