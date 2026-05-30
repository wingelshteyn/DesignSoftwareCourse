"""
verification.models
-------------------
FRQ-6  Operator verification (confirm / reject)
FRQ-7  Manual defect markup

Depends on:
  receiver.InspectionRecord
  detection.DetectedDefect
  accounts.User
"""

from django.db import models
from apps.accounts.models import User
from apps.detection.models import DetectedDefect
from apps.receiver.models import InspectionRecord


class VerificationAction(models.Model):
    """
    Records the operator's final decision and timing for one InspectionRecord.
    Created when the operator submits their verdict.  FRQ-6.3, FRQ-6.4, FRQ-6.5
    """

    class Decision(models.TextChoices):
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    inspection = models.OneToOneField(
        InspectionRecord,
        on_delete=models.CASCADE,
        related_name="verification",
    )
    operator = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="verifications",
        limit_choices_to={"role": User.Role.OPERATOR},
    )
    decision = models.CharField(max_length=20, choices=Decision.choices)
    # Wall-clock duration from image received_at until operator submission  (FRQ-9.2)
    time_to_verify = models.DurationField(
        null=True, blank=True, help_text="Elapsed time from image arrival to verification."
    )
    verified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Verification #{self.pk}: {self.decision} by {self.operator_id}"


class DefectExclusion(models.Model):
    """
    Tracks which auto-detected defects the operator chose to exclude.  FRQ-7.1
    The linked DetectedDefect.is_active is set to False on creation.
    """

    verification = models.ForeignKey(
        VerificationAction,
        on_delete=models.CASCADE,
        related_name="exclusions",
    )
    defect = models.ForeignKey(
        DetectedDefect,
        on_delete=models.CASCADE,
        related_name="exclusions",
    )
    excluded_at = models.DateTimeField(auto_now_add=True)


class ManualDefect(models.Model):
    """
    A defect bounding-box drawn manually by an operator for a missed defect.
    FRQ-7.2, FRQ-7.3
    """

    verification = models.ForeignKey(
        VerificationAction,
        on_delete=models.CASCADE,
        related_name="manual_defects",
    )
    # Type chosen from the DefectType enumeration (same set as DetectedDefect + 'other')
    defect_type = models.CharField(
        max_length=20,
        help_text="Defect type code from administration.DefectType catalog.",
    )
    bbox_x = models.FloatField()
    bbox_y = models.FloatField()
    bbox_w = models.FloatField()
    bbox_h = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"ManualDefect type={self.defect_type} in verification #{self.verification_id}"


class AuditLog(models.Model):
    """
    Append-only structured log of every operator action.
    Provides full traceability (who, when, what).  FRQ-7.4, biz req 3
    """

    class ActionType(models.TextChoices):
        SUBMITTED_VERIFICATION = "submitted_verification", "Submitted Verification"
        EXCLUDED_DEFECT = "excluded_defect", "Excluded Defect"
        ADDED_MANUAL_DEFECT = "added_manual_defect", "Added Manual Defect"

    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
    )
    inspection = models.ForeignKey(
        InspectionRecord,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    action_type = models.CharField(max_length=50, choices=ActionType.choices)
    # Structured payload - e.g. {"defect_id": 42, "type": "RS"}
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"AuditLog {self.action_type} by user #{self.user_id} at {self.timestamp}"
