import factory.fuzzy

from factory.django import DjangoModelFactory

from apps.posts.models import Post
from apps.users.factories.user_factory import UserFactory


class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post

    title = factory.Faker("sentence")
    author = factory.SubFactory(UserFactory)
    body = factory.Faker("sentence")
