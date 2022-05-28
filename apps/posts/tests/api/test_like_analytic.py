import datetime

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from apps.posts.factories.post_factory import PostFactory
from apps.posts.models import Post
from apps.users.factories.token_factory import TokenFactory
from apps.users.factories.user_factory import UserFactory


class AnalyticLikesPostAPITests(TestCase):
    """Test to analytic post's likes API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.post = PostFactory()
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

    def test_analytic_likes_success(self):
        token1 = TokenFactory()
        token2 = TokenFactory()
        date_now = str(datetime.datetime.now().date())

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token1))
        res1 = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(res1.data['message'], 'Post was successfully liked')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(token2))
        res2 = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(res2.data['message'], 'Post was successfully liked')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)

        analytics_res = self.client.get(f'/api/v1/analytic/')
        self.assertEqual(analytics_res.status_code, status.HTTP_200_OK)
        self.assertTrue(analytics_res.data[date_now])
        self.assertEqual(analytics_res.data[date_now]['likes_count'], 2)

    def test_analytic_likes_with_start_date_success(self):
        date_now = str(datetime.datetime.now().date())

        res1 = self.client.get(f'/api/v1/posts/{self.post.id}/like/')
        self.assertEqual(res1.data['message'], 'Post was successfully liked')
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        analytics_res = self.client.get(f'/api/v1/analytic/?start_date={date_now}')
        self.assertEqual(analytics_res.status_code, status.HTTP_200_OK)
        self.assertTrue(analytics_res.data[date_now])
        self.assertEqual(analytics_res.data[date_now]['likes_count'], 1)
