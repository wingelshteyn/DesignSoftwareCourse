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
from .models import AuditLog, VerificationAction
from .serializers import (
    AuditLogSerializer,
    VerificationActionSerializer,
    VerificationSubmitSerializer,
)
from .services import VerificationService


class VerificationSubmitView(APIView):
    """
    POST /api/verification/<inspection_pk>/submit/
    Operator submits verdict + optional markup corrections.  FRQ-6.3–FRQ-7.4
    """

    permission_classes = [IsAdministratorOrOperator]

    def post(self, request, inspection_pk):
        serializer = VerificationSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification = VerificationService.submit_verification(
            inspection_id=inspection_pk,
            operator_id=request.user.pk,
            **serializer.validated_data,
        )
        return Response(
            VerificationActionSerializer(verification).data,
            status=status.HTTP_201_CREATED,
        )


class VerificationDetailView(generics.RetrieveAPIView):
    """GET /api/verification/<inspection_pk>/  - retrieve stored verification."""

    serializer_class = VerificationActionSerializer
    permission_classes = [IsAdministratorOrOperator]

    def get_object(self):
        return VerificationService.get_verification(self.kwargs["inspection_pk"])


class AuditLogListView(generics.ListAPIView):
    """
    GET /api/verification/<inspection_pk>/audit/
    Full action history for one inspection.  FRQ-7.4, biz req 3
    """

    serializer_class = AuditLogSerializer
    permission_classes = [IsAdministratorOrOperator]

    def get_queryset(self):
        return AuditLog.objects.filter(
            inspection_id=self.kwargs["inspection_pk"]
        ).select_related("user")
