"""
analytics.views
---------------
FRQ-8  History + filtering  (all authenticated roles)
FRQ-9  Statistics  (operator: own; technologist+admin: all / per user)
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.accounts.permissions import (
    IsAdministratorOrTechnologist,
    IsOperator,
)
from apps.accounts.models import User
from .serializers import (
    InspectionHistorySerializer,
    OperatorStatisticsSerializer,
    OverallStatisticsSerializer,
)
from .services import HistoryService, StatisticsService


class InspectionHistoryView(APIView):
    """
    GET /api/analytics/history/
    Available to all authenticated roles.  FRQ-8.1
    Accepts query params: status, has_defects, defect_type, date_from, date_to,
                          zone_id, camera_id, operator_id
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        records = HistoryService.list_inspections(
            status=request.query_params.get("status"),
            has_defects=request.query_params.get("has_defects"),
            defect_types=request.query_params.getlist("defect_type"),
            date_from=request.query_params.get("date_from"),
            date_to=request.query_params.get("date_to"),
            zone_id=request.query_params.get("zone_id"),
            camera_id=request.query_params.get("camera_id"),
            operator_id=request.query_params.get("operator_id"),
        )
        return Response(InspectionHistorySerializer(records, many=True).data)


class InspectionDetailView(APIView):
    """
    GET /api/analytics/history/<inspection_pk>/
    Drill-down: full context for one inspection.  FRQ-9.6
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, inspection_pk):
        detail = HistoryService.get_inspection_detail(inspection_pk)
        return Response(detail)


class MyStatisticsView(APIView):
    """
    GET /api/analytics/stats/me/
    Operator's own statistics.  FRQ-9.2
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        stats = StatisticsService.get_operator_statistics(
            operator_id=request.user.pk,
            date_from=request.query_params.get("date_from"),
            date_to=request.query_params.get("date_to"),
        )
        return Response(OperatorStatisticsSerializer(stats).data)


class OverallStatisticsView(APIView):
    """
    GET /api/analytics/stats/
    System-wide statistics (technologist + admin).  FRQ-9.3, FRQ-9.5
    """

    permission_classes = [IsAdministratorOrTechnologist]

    def get(self, request):
        stats = StatisticsService.get_overall_statistics(
            date_from=request.query_params.get("date_from"),
            date_to=request.query_params.get("date_to"),
        )
        return Response(OverallStatisticsSerializer(stats).data)


class UserStatisticsView(APIView):
    """
    GET /api/analytics/stats/users/<user_pk>/
    Per-operator statistics for technologist.  FRQ-9.4, FRQ-9.5
    """

    permission_classes = [IsAdministratorOrTechnologist]

    def get(self, request, user_pk):
        stats = StatisticsService.get_user_statistics(
            user_id=user_pk,
            date_from=request.query_params.get("date_from"),
            date_to=request.query_params.get("date_to"),
        )
        return Response(OperatorStatisticsSerializer(stats).data)
