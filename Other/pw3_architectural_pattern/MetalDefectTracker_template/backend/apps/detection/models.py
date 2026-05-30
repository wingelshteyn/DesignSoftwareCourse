"""
Automatic defect detection pipeline
Status updates on InspectionRecord
"""

from django.db import models
from apps.receiver.models import InspectionRecord


class DefectDetection(models.Model):
    """
    Container for one ML-inference run on a single InspectionRecord
    """

    # inspection = models.OneToOneField(InspectionRecord)
    # ml_model_version
    # raw_response
    # processed_at
    pass


class DetectedDefect(models.Model):
    """
    Single defect bounding-box returned by the ML service
    """

    class DefectType(models.TextChoices):
        ROLLED_IN_SCALE = "RS", "Rolled-in Scale (RS)"
        PATCHES = "Pa", "Patches (Pa)"
        #...

    # detection = models.ForeignKey(DefectDetection)
    # defect_type
    # bbox_x
    # bbox_y
    # bbox_w
    # bbox_h
    # confidence
