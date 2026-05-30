"""
administration.views
--------------------
All views require IsAdministrator permission (NFRQ-1.1).

FRQ-10  Camera configuration
FRQ-11  Defect catalog, grouping 'other', fine-tuning
FRQ-12  Model version deploy / rollback
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdministrator
from .services import (
    CameraConfigService,
    DefectTypeService,
    ModelVersionService,
    RetrainingService,
)


class CameraSettingsView(APIView):
    """
    GET  /api/admin-panel/cameras/<camera_pk>/settings/  - retrieve
    PATCH /api/admin-panel/cameras/<camera_pk>/settings/ - update
    """
    pass


class DefectTypeListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/admin-panel/defect-types/"""
    pass


class ModelVersionListView(generics.ListAPIView):
    """GET /api/admin-panel/model/versions/"""
    pass


class ModelVersionDeployView(APIView):
    """POST /api/admin-panel/model/deploy/  - promote a staging version to active"""

    permission_classes = [IsAdministrator]


class ModelVersionRollbackView(APIView):
    """POST /api/admin-panel/model/rollback/  - restore previous version"""

    permission_classes = [IsAdministrator]


class ConfidenceThresholdView(APIView):
    """PATCH /api/admin-panel/model/<version_pk>/threshold/"""

    permission_classes = [IsAdministrator]


class StartRetrainingView(APIView):
    """POST /api/admin-panel/model/retrain/  - initiate fine-tuning job"""

    permission_classes = [IsAdministrator]


class RetrainingJobDetailView(generics.RetrieveAPIView):
    """GET /api/admin-panel/model/retrain/<pk>/  - poll job status"""
    pass
