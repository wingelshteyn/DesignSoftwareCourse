"""
Camera configuration
Defect type catalog & model fine-tuning
Model version management & rollback
"""

from django.db import models
from apps.accounts.models import User


class CameraSettings(models.Model):
    """
    Configurable parameters for a Camera source
    """

    # camera = models.OneToOneField("receiver.Camera")
    # resolution_width
    # resolution_height
    # capture_interval_seconds
    pass


class DefectType(models.Model):
    """
    Extensible catalog of defect type labels
    """

    # code
    # label
    # description = models.TextField(blank=True)
    # is_builtin = models.BooleanField(default=False)
    pass


class ModelVersion(models.Model):
    """
    Tracks every model artifact available in the system
    """

    class Status(models.TextChoices):
        STAGING = "staging", "Staging"     # uploaded but not yet deployed
        ACTIVE = "active", "Active"        # currently serving inference
        ROLLBACK = "rollback", "Rollback"  # previously active, can be re-activated
        ARCHIVED = "archived", "Archived"  # obsolete

    # version_tag
    # status
    # confidence_threshold
    # artifact_path # MinIO
    # deployed_at


class RetrainingJob(models.Model):
    """
    Tracks an on-demand fine-tuning run
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    # initiated_by = models.ForeignKey(User)
    # status
    # dataset_size
    # base_model_version = models.ForeignKey(ModelVersion)
    # result_model_version = models.ForeignKey(ModelVersion)
