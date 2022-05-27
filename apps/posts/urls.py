from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.posts.api.views import PostViewSet, PostAnalyticView

router = DefaultRouter()

router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path(r'analytic/', PostAnalyticView.as_view(), name='analytic'),
]

urlpatterns += router.urls
