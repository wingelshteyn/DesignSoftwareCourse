"""administration URL patterns"""

from django.urls import path
from .views import (
    CameraSettingsView,
    ConfidenceThresholdView,
    DefectTypeListCreateView,
    DefectTypeOtherGroupView,
    ModelVersionDeployView,
    ModelVersionListView,
    ModelVersionRollbackView,
    RetrainingJobDetailView,
    StartRetrainingView,
)

urlpatterns = [
    path("admin-panel/cameras/<int:camera_pk>/settings/",CameraSettingsView.as_view(),name="camera-settings",),
    path("admin-panel/defect-types/", DefectTypeListCreateView.as_view(), name="defect-type-list"),
    path("admin-panel/defect-types/other-group/", DefectTypeOtherGroupView.as_view(), name="defect-type-other"),
    path("admin-panel/model/versions/", ModelVersionListView.as_view(), name="model-versions"),
    path("admin-panel/model/deploy/", ModelVersionDeployView.as_view(), name="model-deploy"),
    path("admin-panel/model/rollback/", ModelVersionRollbackView.as_view(), name="model-rollback"),
    path("admin-panel/model/<int:version_pk>/threshold/", ConfidenceThresholdView.as_view(), name="model-threshold"),
    path("admin-panel/model/retrain/", StartRetrainingView.as_view(), name="model-retrain"),
    path("admin-panel/model/retrain/<int:pk>/", RetrainingJobDetailView.as_view(), name="model-retrain-detail"),
]
