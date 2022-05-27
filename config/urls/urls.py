from django.contrib import admin
from django.urls import path, include

from config.urls import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('config.urls.api_router')),
] + swagger.urlpatterns
