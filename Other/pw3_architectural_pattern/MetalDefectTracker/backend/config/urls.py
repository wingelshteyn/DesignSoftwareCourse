"""
Root URL configuration for MetalDefectTracker.

All API routes are prefixed with /api/ and delegated to the corresponding app.
React SPA is served by Nginx at / (not Django).

Route map:
  /api/auth/          -> accounts app  (JWT token endpoints)
  /api/users/         -> accounts app  (user management)
  /api/zones/         -> accounts app  (zones / areas)
  /api/images/        -> receiver app  (image ingestion & inspection records)
  /api/detections/    -> detection app (detection results per inspection)
  /api/verification/  -> verification app (operator actions)
  /api/analytics/     -> analytics app (statistics, history)
  /api/admin-panel/   -> administration app (camera, model, defect types)
  /api/schema/        -> drf-spectacular OpenAPI schema
  /api/docs/          -> Swagger UI
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Django admin (internal tooling)
    path("django-admin/", admin.site.urls),

    # OpenAPI schema & Swagger UI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # Application API routes
    path("api/", include("apps.accounts.urls")),
    path("api/", include("apps.receiver.urls")),
    path("api/", include("apps.detection.urls")),
    path("api/", include("apps.verification.urls")),
    path("api/", include("apps.analytics.urls")),
    path("api/", include("apps.administration.urls")),
]
