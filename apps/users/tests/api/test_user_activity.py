import datetime

from django.urls import reverse
from django.test import TestCase
from django.utils.dateparse import parse_datetime
from rest_framework.test import APIClient
from rest_framework import status

from apps.users.factories.token_factory import TokenFactory

ACTIVITY_URL = reverse('user_activity')


class UserActivityAPITests(TestCase):
    """Test to user activity API"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.token = TokenFactory()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

    def test_user_activity_last_request_successful(self):
        """
        Test to check user last request successful
        """
        self.client.get(ACTIVITY_URL)
        request_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        response_second = self.client.get(ACTIVITY_URL)
        response_time = parse_datetime(response_second.data['last_request']).strftime("%d/%m/%Y %H:%M")
        self.assertEqual(response_second.status_code, status.HTTP_200_OK)
        self.assertEqual(response_time, request_time)

