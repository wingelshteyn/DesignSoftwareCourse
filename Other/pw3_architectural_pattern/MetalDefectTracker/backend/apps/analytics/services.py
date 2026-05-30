"""
analytics.services
------------------
Public API of the analytics module.
FRQ-8  History listing and filtering
FRQ-9  Statistics and aggregated reports

All queries aggregate data from receiver, detection, and verification tables
via Django ORM. No data is stored in analytics-owned tables.

Inter-module access:
  - Imports InspectionRecord from receiver via public model import
    (analytics is a read-only consumer - no writes to other modules' tables)
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from apps.receiver.models import InspectionRecord


class HistoryService:
    """
    Filtered listing and drill-down on inspection history.
    FRQ-8.1–FRQ-8.7
    """

    @staticmethod
    def list_inspections(
        status: str | None = None,
        has_defects: bool | None = None,
        defect_types: list[str] | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
        zone_id: int | None = None,
        camera_id: int | None = None,
        operator_id: int | None = None,
    ) -> list["InspectionRecord"]:
        """
        Return filtered InspectionRecords.
        Filtering params correspond to FRQ-8.2–FRQ-8.7.
        """
        raise NotImplementedError

    @staticmethod
    def get_inspection_detail(inspection_id: int) -> dict:
        """
        Full drill-down for one inspection: record + detection + verification.
        Powers the 'drill-down from statistics' use case.  FRQ-9.6
        """
        raise NotImplementedError


class StatisticsService:
    """
    Aggregated statistical reports.  FRQ-9.1–FRQ-9.6
    """

    @staticmethod
    def get_operator_statistics(operator_id: int, date_from=None, date_to=None) -> dict:
        """
        Per-operator stats: images processed, defects found, avg verification time.
        FRQ-9.2
        """
        raise NotImplementedError

    @staticmethod
    def get_overall_statistics(date_from=None, date_to=None) -> dict:
        """
        System-wide stats used by technologist dashboard.
        Includes breakdown by defect type, operator, zone.  FRQ-9.3
        """
        raise NotImplementedError

    @staticmethod
    def get_user_statistics(user_id: int, date_from=None, date_to=None) -> dict:
        """
        Statistics for a specific operator - used by technologist.  FRQ-9.4
        """
        raise NotImplementedError
