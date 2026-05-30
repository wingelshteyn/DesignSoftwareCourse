"""
Root URL configuration for MetalDefectTracker.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.receiver.urls")),
    path("api/", include("apps.detection.urls")),
    path("api/", include("apps.verification.urls")),
    path("api/", include("apps.analytics.urls")),
    path("api/", include("apps.administration.urls")),
]
