"""detection URL patterns"""

from django.urls import path
from .views import DefectDetectionDetailView

urlpatterns = [
    path("detections/<int:inspection_pk>/", DefectDetectionDetailView.as_view(), name="detection-detail"),
]
