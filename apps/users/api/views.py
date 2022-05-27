from django.contrib.auth import get_user_model
from rest_framework import generics, authentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from django.contrib.auth.models import update_last_login
from apps.users.api.serializers import UserRegistrationSerializer, UserLoginSerializer, UserActivitySerializer, \
    UserDetailSerializer

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer


class UserLoginAPIView(ObtainAuthToken):
    """
    Endpoint to login user in system
    """
    serializer_class = UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        """
        Endpoint to authenticate user
        @return: user data and user token
        """
        response = super(UserLoginAPIView, self).post(request, *args, **kwargs)

        token = Token.objects.get(key=response.data['token'])
        update_last_login(None, token.user)
        user = UserDetailSerializer(token.user)
        return Response({'token': token.key, 'user': user.data})


class UserActivityView(generics.RetrieveAPIView):
    serializer_class = UserActivitySerializer
    authentication_classes = [authentication.TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
