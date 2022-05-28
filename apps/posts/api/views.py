from datetime import datetime

from django.db.models import Count
from rest_framework import viewsets, authentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.posts.api.serializers import PostSerializer
from apps.posts.models import Post, Like


class PostViewSet(viewsets.ModelViewSet):
    """
    Post viewsets
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new post"""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def like(self, request, pk):
        try:
            post = Post.objects.get(id=pk)
            liked_obj = Like.objects.filter(post=post, user=request.user)
            if liked_obj.exists():
                liked_obj.delete()
                return Response({'message': 'Post was successfully unliked'})
            Like.objects.create(post=post, user=request.user)
            return Response({'message': 'Post was successfully liked'})
        except Exception as e:
            return Response({'message': f'{e}'})


class PostAnalyticView(APIView):
    """
    View to analyse Post's likes
    """
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        date = {}
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', datetime.now())
        likes = Like.objects.all()
        if start_date:
            likes = Like.objects.filter(liked_at__range=[start_date, end_date])

        likes_counter = likes \
            .values('liked_at__date') \
            .annotate(likes_number=Count('id'))
        for like in likes_counter:
            date[f"{like['liked_at__date']}"] = {'likes_count': like['likes_number']}
        return Response(date)
