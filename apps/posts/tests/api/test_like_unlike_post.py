from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.posts.factories.post_factory import PostFactory
from apps.posts.models import Post
from apps.users.factories.token_factory import TokenFactory
from apps.users.factories.user_factory import UserFactory


class LikePostAPITests(TestCase):
    """Test the post create API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = UserFactory()
        self.post = PostFactory()
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

    def test_like_post_successful(self):
        response = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post was successfully liked')
        post_liked = self.client.get(f'/api/v1/posts/{self.post.id}/').data['likes']
        self.assertEqual(post_liked, 1)

    def test_unlike_post_successful(self):
        self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        response = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Post was successfully unliked')
        post_liked = self.client.get(f'/api/v1/posts/{self.post.id}/').data['likes']
        self.assertEqual(post_liked, 0)

    def test_like_unlike_unauthenticated_failed(self):
        client = APIClient()
        response = client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_with_multiple_user_success(self):
        token1 = TokenFactory()
        token2 = TokenFactory()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token1))
        res1 = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(res1.data['message'], 'Post was successfully liked')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token2))
        res2 = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(res2.data['message'], 'Post was successfully liked')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

        post_liked = self.client.get(f'/api/v1/posts/{self.post.id}/').data['likes']
        self.assertEqual(post_liked, 2)
