from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer to register new user with token"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password")

    def validate(self, attrs):
        attrs['password'] = make_password(attrs['password'])
        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer to user public views
    """

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'is_staff')


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer to user activity view
    """

    class Meta:
        model = get_user_model()
        fields = ('email', 'last_login', 'last_request')


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user authentication object
    """

    def __init__(self, *args, **kwargs):
        """Initialize serializer"""
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    email = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        self.user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not self.user:
            """Statement to check result of authenticate"""
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = self.user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    """Serializer to authentication token"""
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('auth_token',)
