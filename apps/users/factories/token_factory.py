import factory
from factory.django import DjangoModelFactory
from rest_framework.authtoken.models import Token

from apps.users.factories.user_factory import UserFactory


class TokenFactory(DjangoModelFactory):
    """
    Create fake User model
    """

    class Meta:
        model = Token
    user = factory.SubFactory(UserFactory)
