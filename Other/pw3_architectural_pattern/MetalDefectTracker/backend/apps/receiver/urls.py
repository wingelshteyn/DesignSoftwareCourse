"""receiver URL patterns"""

from django.urls import path
from .views import (
    CameraListCreateView,
    ImageIngestView,
    InspectionRecordDetailView,
    InspectionRecordListView,
)

urlpatterns = [
    # Image ingestion  (FRQ-3.1)
    path("images/", ImageIngestView.as_view(), name="image-ingest"),
    # History  (FRQ-8.1) - full list returned here; filtering in analytics
    path("images/list/", InspectionRecordListView.as_view(), name="inspection-list"),
    path("images/<int:pk>/", InspectionRecordDetailView.as_view(), name="inspection-detail"),
    # Camera registry  (FRQ-10)
    path("cameras/", CameraListCreateView.as_view(), name="camera-list-create"),
]
