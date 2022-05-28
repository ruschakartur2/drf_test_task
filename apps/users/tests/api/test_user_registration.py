from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.users.factories.user_factory import UserFactory

REGISTER_USER_URL = reverse("auth_register")

User = get_user_model()


class UserRegisterAPITests(TestCase):
    """Test the user registration API"""

    def setUp(self) -> None:
        self.client = APIClient()

        self.email = "test@test.com"
        self.password = "fhnehheofr555605"

        self.payload = {
            "email": self.email,
            "password": self.password,
        }

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful created"""
        response = self.client.post(REGISTER_USER_URL, self.payload)

        created_user = User.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(created_user.email, self.email)

    def test_create_user_email_unique(self):
        """Test create user that already exists fails"""
        UserFactory.create(email=self.email)

        response = self.client.post(REGISTER_USER_URL, self.payload)
        self.assertEqual(
            response.data["email"][0], "user with this User's email address already exists."
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_without_email(self):
        """Test create user without email fails"""
        payload = {
            "password": self.password,
        }
        response = self.client.post(REGISTER_USER_URL, payload)
        self.assertEqual(response.data["email"][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
