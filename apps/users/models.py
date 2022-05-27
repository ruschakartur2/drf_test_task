from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

from apps.users.managers.users import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(verbose_name=_("User's status (online/offline)"), default=True)
    is_staff = models.BooleanField(verbose_name=_("User's admin status"), default=False)
    is_superuser = models.BooleanField(verbose_name=_("User's superuser status"), default=False)
    is_muted = models.BooleanField(verbose_name=_("User muted"), default=False)
    email = models.EmailField(verbose_name=_("User's email address"),
                              max_length=255,
                              unique=True)
    last_request = models.DateTimeField(auto_now=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def __str__(self):
        """Function to naming model"""
        return self.email