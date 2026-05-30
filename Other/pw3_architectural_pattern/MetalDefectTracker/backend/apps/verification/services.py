"""
verification.services
---------------------
Public API of the verification module.
FRQ-6  Operator verification
FRQ-7  Manual defect markup

All verification state changes go through this service.
It writes AuditLog entries and updates InspectionRecord.status
via receiver.services (never touching receiver DB directly).
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import AuditLog, DefectExclusion, ManualDefect, VerificationAction
    from apps.accounts.models import User
    from apps.receiver.models import InspectionRecord


class VerificationService:
    """Handles the full operator verification workflow.  FRQ-6, FRQ-7"""

    @staticmethod
    def submit_verification(
        inspection_id: int,
        operator_id: int,
        decision: str,
        excluded_defect_ids: list[int] | None = None,
        manual_defects: list[dict] | None = None,
    ) -> "VerificationAction":
        """
        Atomic operation:
          1. Create VerificationAction with decision.
          2. Create DefectExclusion rows and mark DetectedDefects inactive.  FRQ-7.1
          3. Create ManualDefect rows.  FRQ-7.2, FRQ-7.3
          4. Update InspectionRecord.status → accepted / rejected.
          5. Write AuditLog entries.  FRQ-7.4
        """
        raise NotImplementedError

    @staticmethod
    def get_verification(inspection_id: int) -> "VerificationAction":
        raise NotImplementedError


class AuditService:
    """Append-only audit trail.  FRQ-7.4"""

    @staticmethod
    def log_action(
        user_id: int,
        inspection_id: int,
        action_type: str,
        details: dict | None = None,
    ) -> "AuditLog":
        raise NotImplementedError

    @staticmethod
    def get_inspection_history(inspection_id: int) -> list["AuditLog"]:
        raise NotImplementedError
