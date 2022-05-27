from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.factories.user_factory import UserFactory

LOGIN_USER_URL = reverse("auth_login")

User = get_user_model()


class UserLoginAPITests(TestCase):
    """Test the user registration API"""

    def setUp(self) -> None:
        self.client = APIClient()

        self.email = "test@test.com"
        self.password = "test123test2"

        self.payload = {
            "email": self.email,
            "password": self.password,
        }

        self.user = UserFactory(email=self.email, password=self.password)

    def test_login_user_successful(self):
        """Test to login user is successful"""
        response = self.client.post(LOGIN_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user']['email'], self.email)

    def test_login_user_with_invalid_credentials(self):
        """Test to login user with invalid credentials is failure"""
        self.payload["password"] = "wrong password"

        response = self.client.post(LOGIN_USER_URL, self.payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)