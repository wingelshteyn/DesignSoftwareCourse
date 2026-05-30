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
    IsAdministratorOrOperator,
)
from .services import HistoryService, StatisticsService


class InspectionHistoryView(APIView):
    """
    GET /api/analytics/history/
    """

    permission_classes = [IsAuthenticated]


class InspectionDetailView(APIView):
    """
    GET /api/analytics/history/<inspection_pk>/
    """

    permission_classes = [IsAuthenticated]


class MyStatisticsView(APIView):
    """
    GET /api/analytics/stats/me/
    """

    permission_classes = [IsAuthenticated]


class OverallStatisticsView(APIView):
    """
    GET /api/analytics/stats/
    """

    permission_classes = [IsAdministratorOrTechnologist]


class UserStatisticsView(APIView):
    """
    GET /api/analytics/stats/users/<user_pk>/
    """

    permission_classes = [IsAdministratorOrOperator]
