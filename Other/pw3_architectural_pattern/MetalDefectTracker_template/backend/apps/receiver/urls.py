"""receiver URL patterns"""

from django.urls import path
from .views import (
    CameraListCreateView,
    ImageIngestView,
    InspectionRecordDetailView,
    InspectionRecordListView,
)

urlpatterns = [
    path("images/", ImageIngestView.as_view(), name="image-ingest"),
    path("images/list/", InspectionRecordListView.as_view(), name="inspection-list"),
    path("images/<int:pk>/", InspectionRecordDetailView.as_view(), name="inspection-detail"),
    path("cameras/", CameraListCreateView.as_view(), name="camera-list-create"),
]
