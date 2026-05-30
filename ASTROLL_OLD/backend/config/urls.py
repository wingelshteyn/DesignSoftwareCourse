from django.urls import path

from apps.views import health


urlpatterns = [
    path("api/health", health),
]
