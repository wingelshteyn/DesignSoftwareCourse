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
from .models import DefectType, ModelVersion, RetrainingJob
from .serializers import (
    CameraSettingsSerializer,
    ConfidenceThresholdSerializer,
    DefectTypeSerializer,
    ModelVersionDeploySerializer,
    ModelVersionSerializer,
    RetrainingJobSerializer,
    StartRetrainingSerializer,
)
from .services import (
    CameraConfigService,
    DefectTypeService,
    ModelVersionService,
    RetrainingService,
)


# ---------------------------------------------------------------------------
# Camera settings  (FRQ-10)
# ---------------------------------------------------------------------------


class CameraSettingsView(APIView):
    """
    GET  /api/admin-panel/cameras/<camera_pk>/settings/  - retrieve
    PATCH /api/admin-panel/cameras/<camera_pk>/settings/ - update  FRQ-10.2, FRQ-10.3
    """

    permission_classes = [IsAdministrator]

    def get(self, request, camera_pk):
        settings = CameraConfigService.get_or_create_settings(camera_pk)
        return Response(CameraSettingsSerializer(settings).data)

    def patch(self, request, camera_pk):
        serializer = CameraSettingsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        settings = CameraConfigService.update_settings(
            camera_id=camera_pk, **serializer.validated_data
        )
        return Response(CameraSettingsSerializer(settings).data)


# ---------------------------------------------------------------------------
# Defect type catalog  (FRQ-11.2)
# ---------------------------------------------------------------------------


class DefectTypeListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/admin-panel/defect-types/"""

    queryset = DefectType.objects.all()
    serializer_class = DefectTypeSerializer
    permission_classes = [IsAdministrator]


class DefectTypeOtherGroupView(APIView):
    """
    GET /api/admin-panel/defect-types/other-group/
    Returns grouped ManualDefects with type='other' for reclassification.  FRQ-11.3
    """

    permission_classes = [IsAdministrator]

    def get(self, request):
        groups = DefectTypeService.get_other_defect_images()
        return Response(groups)


# ---------------------------------------------------------------------------
# Model versions  (FRQ-12)
# ---------------------------------------------------------------------------


class ModelVersionListView(generics.ListAPIView):
    """GET /api/admin-panel/model/versions/"""

    queryset = ModelVersion.objects.all()
    serializer_class = ModelVersionSerializer
    permission_classes = [IsAdministrator]


class ModelVersionDeployView(APIView):
    """POST /api/admin-panel/model/deploy/  - promote a staging version to active.  FRQ-12.2"""

    permission_classes = [IsAdministrator]

    def post(self, request):
        serializer = ModelVersionDeploySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        version = ModelVersionService.deploy_version(serializer.validated_data["version_id"])
        return Response(ModelVersionSerializer(version).data)


class ModelVersionRollbackView(APIView):
    """POST /api/admin-panel/model/rollback/  - restore previous version.  FRQ-12.2, NFRQ-3.1"""

    permission_classes = [IsAdministrator]

    def post(self, request):
        serializer = ModelVersionDeploySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        version = ModelVersionService.rollback(serializer.validated_data["version_id"])
        return Response(ModelVersionSerializer(version).data)


class ConfidenceThresholdView(APIView):
    """PATCH /api/admin-panel/model/<version_pk>/threshold/  FRQ-11.1"""

    permission_classes = [IsAdministrator]

    def patch(self, request, version_pk):
        serializer = ConfidenceThresholdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        version = ModelVersionService.set_confidence_threshold(
            version_id=version_pk,
            threshold=serializer.validated_data["confidence_threshold"],
        )
        return Response(ModelVersionSerializer(version).data)


# ---------------------------------------------------------------------------
# Fine-tuning / retraining  (FRQ-11.4)
# ---------------------------------------------------------------------------


class StartRetrainingView(APIView):
    """POST /api/admin-panel/model/retrain/  - initiate fine-tuning job.  FRQ-11.4"""

    permission_classes = [IsAdministrator]

    def post(self, request):
        serializer = StartRetrainingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = RetrainingService.initiate_retraining(
            initiated_by_id=request.user.pk,
            inspection_ids=serializer.validated_data["inspection_ids"],
            base_version_id=serializer.validated_data["base_version_id"],
        )
        return Response(RetrainingJobSerializer(job).data, status=status.HTTP_202_ACCEPTED)


class RetrainingJobDetailView(generics.RetrieveAPIView):
    """GET /api/admin-panel/model/retrain/<pk>/  - poll job status."""

    queryset = RetrainingJob.objects.all()
    serializer_class = RetrainingJobSerializer
    permission_classes = [IsAdministrator]
