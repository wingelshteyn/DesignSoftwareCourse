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


class ImageIngestView(APIView):
    """
    POST /api/images/  - camera pushes a new image for inspection.
    """

    parser_classes = [MultiPartParser]


class InspectionRecordListView(generics.ListAPIView):
    """GET /api/images/  - list inspection records (used by history / analytics)."""
    pass


class InspectionRecordDetailView(generics.RetrieveAPIView):
    """GET /api/images/<pk>/  - single record with full context."""
    pass


class CameraListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/cameras/  - manage camera registry."""
    pass
