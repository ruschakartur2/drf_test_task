import datetime

from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.models import User


class UpdateLastActivityMiddleware(object):
    """
    Middleware to track user activity
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(request.user)
        if request.user.id:
            get_user_model().objects.filter(id=request.user.id).update(last_request=timezone.now())
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request,
                       'user'), 'The UpdateLastActivityMiddleware requires authentication middleware to be installed.'
