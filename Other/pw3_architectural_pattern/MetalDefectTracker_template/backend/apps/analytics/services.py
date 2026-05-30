"""
Public API of the analytics module
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.receiver.models import InspectionRecord


class HistoryService:
    """
    Filtered listing and drill-down on inspection history
    """

    def list_inspections():
        pass

    def get_inspection_detail():
        pass


class StatisticsService:
    """
    Aggregated statistical reports
    """

    def get_operator_statistics():
        pass

    def get_overall_statistics():
        pass

    def get_user_statistics():
        pass
