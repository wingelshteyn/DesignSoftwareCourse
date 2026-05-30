"""
receiver.views
--------------
FRQ-3   Image ingestion endpoint called by cameras.
FRQ-5   InspectionRecord status is queued immediately on 202 response.
"""

from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.permissions import IsAdministrator
from .models import Camera, InspectionRecord
from .serializers import CameraSerializer, ImageUploadSerializer, InspectionRecordSerializer
from .services import ImageReceiverService


class ImageIngestView(APIView):
    """
    POST /api/images/  - camera pushes a new image for inspection.
    Returns 202 Accepted immediately; detection runs asynchronously.  FRQ-3.1
    """

    parser_classes = [MultiPartParser]
    # Camera clients authenticate with a dedicated service token (operator-level)
    # Actual auth mechanism TBD (e.g. API key header)

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        record = ImageReceiverService.receive_image(
            camera_id=serializer.validated_data["camera_id"],
            image_file=serializer.validated_data["image"],
        )
        return Response(
            InspectionRecordSerializer(record).data,
            status=status.HTTP_202_ACCEPTED,
        )


class InspectionRecordListView(generics.ListAPIView):
    """GET /api/images/  - list inspection records (used by history / analytics)."""

    serializer_class = InspectionRecordSerializer

    def get_queryset(self):
        return InspectionRecord.objects.select_related("camera__zone").all()


class InspectionRecordDetailView(generics.RetrieveAPIView):
    """GET /api/images/<pk>/  - single record with full context."""

    queryset = InspectionRecord.objects.select_related("camera__zone").all()
    serializer_class = InspectionRecordSerializer


# ---------------------------------------------------------------------------
# Camera registration  (administrator)
# ---------------------------------------------------------------------------


class CameraListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/cameras/  - manage camera registry."""

    queryset = Camera.objects.select_related("zone").all()
    serializer_class = CameraSerializer
    permission_classes = [IsAdministrator]
