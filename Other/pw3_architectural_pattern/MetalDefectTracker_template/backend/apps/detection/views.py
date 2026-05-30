"""
detection.views
---------------
Read-only endpoints exposing detection results per inspection.
FRQ-4.2, FRQ-6.2
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import DefectDetectionSerializer


class DefectDetectionDetailView(generics.RetrieveAPIView):
    """
    GET /api/detections/<inspection_pk>/
    """

    serializer_class = DefectDetectionSerializer
    permission_classes = [IsAuthenticated]
