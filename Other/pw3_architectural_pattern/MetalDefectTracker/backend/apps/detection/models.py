"""
detection.models
----------------
FRQ-4  Automatic defect detection pipeline
FRQ-5  Status updates on InspectionRecord

Depends on:
  receiver.InspectionRecord  (OneToOne: DefectDetection -> InspectionRecord)
"""

from django.db import models
from apps.receiver.models import InspectionRecord


class DefectDetection(models.Model):
    """
    Container for one ML-inference run on a single InspectionRecord.
    Raw JSON response from the ML service is preserved for audit.  FRQ-4.2
    """

    inspection = models.OneToOneField(
        InspectionRecord,
        on_delete=models.CASCADE,
        related_name="detection",
    )
    # Version tag of the ML model that produced this result (FRQ-12)
    ml_model_version = models.CharField(max_length=50, blank=True)
    # Full JSON response preserved for traceability  (FRQ-3 biz req 3)
    raw_response = models.JSONField(default=dict)
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Detection for inspection #{self.inspection_id}"


class DetectedDefect(models.Model):
    """
    Single defect bounding-box returned by the ML service.  FRQ-4.2, FRQ-4.3
    is_active=False when the operator excludes this defect.  FRQ-7.1
    """

    class DefectType(models.TextChoices):
        ROLLED_IN_SCALE = "RS", "Rolled-in Scale (RS)"
        PATCHES = "Pa", "Patches (Pa)"
        CRAZING = "Cr", "Crazing (Cr)"
        PITTED_SURFACE = "PS", "Pitted Surface (PS)"
        INCLUSION = "In", "Inclusion (In)"
        SCRATCHES = "Sc", "Scratches (Sc)"
        OTHER = "other", "Other"

    detection = models.ForeignKey(
        DefectDetection,
        on_delete=models.CASCADE,
        related_name="defects",
    )
    defect_type = models.CharField(max_length=20, choices=DefectType.choices)
    # Bounding box in pixels (top-left x/y, width, height)
    bbox_x = models.FloatField()
    bbox_y = models.FloatField()
    bbox_w = models.FloatField()
    bbox_h = models.FloatField()
    confidence = models.FloatField(help_text="ML confidence score [0, 1].")
    # Operator sets this to False when excluding the defect  (FRQ-7.1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-confidence"]

    def __str__(self) -> str:
        return f"{self.defect_type} @ ({self.bbox_x:.0f},{self.bbox_y:.0f}) conf={self.confidence:.2f}"
