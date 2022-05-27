from django.test import TestCase

from apps.posts.factories.post_factory import PostFactory


class PostModelTests(TestCase):
    def setUp(self):
        self.clan = PostFactory.create(title="Some Title")

    def test_string_representation(self):
        self.assertEqual("Some Title", str(self.clan))
