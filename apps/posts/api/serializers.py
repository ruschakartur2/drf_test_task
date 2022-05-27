from rest_framework import serializers

from apps.posts.models import Post, Like
from apps.users.api.serializers import UserDetailSerializer


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer to Post model
    """

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    author = UserDetailSerializer(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_likes(instance):
        return instance.post_likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
