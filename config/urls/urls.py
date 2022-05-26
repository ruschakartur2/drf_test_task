from django.contrib import admin
from django.urls import path

from config.urls import swagger

urlpatterns = [
    path('admin/', admin.site.urls),
] + swagger.urlpatterns
