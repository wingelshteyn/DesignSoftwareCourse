"""verification URL patterns"""

from django.urls import path
from .views import AuditLogListView, VerificationDetailView, VerificationSubmitView

urlpatterns = [
    path("verification/<int:inspection_pk>/", VerificationDetailView.as_view(), name="verification-detail"),
    path("verification/<int:inspection_pk>/submit/", VerificationSubmitView.as_view(), name="verification-submit"),
    path("verification/<int:inspection_pk>/audit/", AuditLogListView.as_view(), name="verification-audit"),
]
