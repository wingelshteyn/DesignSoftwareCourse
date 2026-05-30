"""
Operator verification (confirm / reject)
Manual defect markup
"""

from django.db import models
from apps.accounts.models import User
from apps.detection.models import DetectedDefect
from apps.receiver.models import InspectionRecord


class VerificationAction(models.Model):
    """
    Records the operator's final decision and timing for one InspectionRecord
    """

    class Decision(models.TextChoices):
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    # inspection = models.OneToOneField(InspectionRecord)
    # operator = models.ForeignKey(User)
    # decision
    # time_to_verify
    # verified_at


class DefectExclusion(models.Model):
    """
    Tracks which auto-detected defects the operator chose to exclude
    """

    # verification = models.ForeignKey(VerificationAction)
    # defect = models.ForeignKey(DetectedDefect)
    # excluded_at = models.DateTimeField(auto_now_add=True)
    pass


class ManualDefect(models.Model):
    """
    A defect bounding-box drawn manually by an operator for a missed defect
    """

    # verification = models.ForeignKey(VerificationAction)
    # defect_type
    # bbox_x
    # bbox_y
    # bbox_w
    # bbox_h
    # created_at
    pass


class AuditLog(models.Model):
    """
    Append-only structured log of every operator action
    """

    class ActionType(models.TextChoices):
        SUBMITTED_VERIFICATION = "submitted_verification", "Submitted Verification"
        EXCLUDED_DEFECT = "excluded_defect", "Excluded Defect"
        ADDED_MANUAL_DEFECT = "added_manual_defect", "Added Manual Defect"

    # user = models.ForeignKey(User)
    # inspection = models.ForeignKey(InspectionRecord)
    # action_type
    # details
    # timestamp
