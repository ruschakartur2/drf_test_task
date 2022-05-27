from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator


class Post(models.Model):
    title = models.CharField(verbose_name=_("Post's title"),
                             max_length=255,
                             unique=True, validators=[MinLengthValidator(3)])
    created_at = models.DateTimeField(verbose_name=_("Article's created time"),
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Article's updated time"),
                                      auto_now=True)
    author = models.ForeignKey(get_user_model(),
                               verbose_name=_("Article's author"),
                               on_delete=models.DO_NOTHING)
    body = models.TextField(verbose_name=_("Article's body"), validators=[MinLengthValidator(10)])
    likes = models.ManyToManyField(get_user_model(), related_name='blogpost_like')

    def __str__(self):
        """Function to naming model"""
        return self.title


class Like(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_likes')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_likes')
    liked_at = models.DateTimeField(auto_now=True)
