"""
verification.views
------------------
FRQ-6  Operator verification submit + retrieve
FRQ-7  Markup corrections (included in submit payload)
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics

from apps.accounts.permissions import IsAdministratorOrOperator


class VerificationSubmitView(APIView):
    """
    POST /api/verification/<inspection_pk>/submit/
    """

    permission_classes = [IsAdministratorOrOperator]


class VerificationDetailView(generics.RetrieveAPIView):
    """GET /api/verification/<inspection_pk>/  - retrieve stored verification."""
    pass


class AuditLogListView(generics.ListAPIView):
    """
    GET /api/verification/<inspection_pk>/audit/
    """
    pass
