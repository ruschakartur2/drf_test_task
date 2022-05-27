from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.posts.models import Post
from apps.users.factories.token_factory import TokenFactory
from apps.users.factories.user_factory import UserFactory

POSTS_URL = reverse("posts-list")
LOGIN_URL = reverse("auth_login")
REGISTER_URL = reverse("auth_register")


class CreatePostAPITests(TestCase):
    """Test the post create API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserFactory()
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))


    def test_create_new_post_successful(self):
        payload = {
            "title": "testtitle",
            "body": "test description here",
        }
        response = self.client.post(POSTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post_in_db = Post.objects.get(id=response.data["id"])

        self.assertEqual(payload["title"], post_in_db.title)
        self.assertEqual(payload["body"], post_in_db.body)
        self.assertEqual(payload["title"], response.data["title"])
        self.assertEqual(payload["body"], response.data["body"])

    def test_create_new_post_with_unauthorized_user_failed(self):
        payload = {}
        self.client.logout()
        response = self.client.post(POSTS_URL, payload)
        self.assertEqual(
            response.data["detail"], "Authentication credentials were not provided."
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_new_post_without_title(self):
        payload = {
            "body": "test description here",
        }
        response = self.client.post(POSTS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("This field is required.", response.data["title"][0])
