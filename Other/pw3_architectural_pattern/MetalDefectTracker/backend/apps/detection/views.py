"""
detection.views
---------------
Read-only endpoints exposing detection results per inspection.
FRQ-4.2, FRQ-6.2
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import DefectDetection
from .serializers import DefectDetectionSerializer


class DefectDetectionDetailView(generics.RetrieveAPIView):
    """
    GET /api/detections/<inspection_pk>/
    Returns detection result (list of bboxes) for a given inspection.
    Used by the operator verification UI to display defect overlays.  FRQ-6.2
    """

    serializer_class = DefectDetectionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        from .services import DetectionService
        return DetectionService.get_detection_result(
            self.kwargs["inspection_pk"]
        )
