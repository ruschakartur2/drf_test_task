from django.urls import include, path

urlpatterns = [
    path('', include('apps.posts.urls')),
    path('users/', include('apps.users.urls')),
]
