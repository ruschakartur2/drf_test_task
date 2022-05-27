from django.urls import path

from apps.users.api.views import UserLoginAPIView, UserRegisterView, UserActivityView

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='auth_login'),
    path('register/', UserRegisterView.as_view(), name='auth_register'),
    path('activity/', UserActivityView.as_view(), name='user_activity')
]
