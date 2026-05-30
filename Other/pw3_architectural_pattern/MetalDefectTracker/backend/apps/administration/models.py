"""
administration.models
---------------------
FRQ-10  Camera configuration
FRQ-11  Defect type catalog & model fine-tuning
FRQ-12  Model version management & rollback

Depends on:
  receiver.Camera  (OneToOne: CameraSettings -> Camera)
  accounts.User    (ForeignKey: RetrainingJob -> User)
"""

from django.db import models
from apps.accounts.models import User


class CameraSettings(models.Model):
    """
    Configurable parameters for a Camera source.  FRQ-10.1, FRQ-10.2, FRQ-10.3
    Separated from Camera to keep receiver.Camera lightweight.
    """

    # Lazy FK via string to avoid circular import with receiver
    camera = models.OneToOneField(
        "receiver.Camera",
        on_delete=models.CASCADE,
        related_name="settings",
    )
    resolution_width = models.PositiveIntegerField(default=1920)    # FRQ-10.2
    resolution_height = models.PositiveIntegerField(default=1080)   # FRQ-10.2
    capture_interval_seconds = models.FloatField(default=5.0)       # FRQ-10.3
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return (
            f"Settings for {self.camera}: "
            f"{self.resolution_width}x{self.resolution_height} every {self.capture_interval_seconds}s"
        )


class DefectType(models.Model):
    """
    Extensible catalog of defect type labels.  FRQ-11.2
    Built-in types (RS, Pa, Cr, PS, In, Sc, other) are pre-populated via migration.
    Administrators can add new types as production evolves.
    """

    code = models.CharField(max_length=20, unique=True)   # e.g. "RS", "Cr"
    label = models.CharField(max_length=100)              # e.g. "Rolled-in Scale"
    description = models.TextField(blank=True)
    # Prevents accidental deletion of factory-seeded types
    is_builtin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.label}"


class ModelVersion(models.Model):
    """
    Tracks every model artifact available in the system.  FRQ-12.1, FRQ-12.2
    Kubernetes rolling-update deploys a new pod for the active version;
    rollback sets the previous version back to ACTIVE.
    """

    class Status(models.TextChoices):
        STAGING = "staging", "Staging"     # uploaded but not yet deployed
        ACTIVE = "active", "Active"        # currently serving inference
        ROLLBACK = "rollback", "Rollback"  # previously active, can be re-activated
        ARCHIVED = "archived", "Archived"  # obsolete

    version_tag = models.CharField(max_length=50, unique=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.STAGING
    )
    # Confidence threshold forwarded to ML service config  (FRQ-11.1)
    confidence_threshold = models.FloatField(default=0.5)
    # MinIO object key of the serialised model file (ONNX / PyTorch)
    artifact_path = models.CharField(max_length=500)
    deployed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"ModelVersion {self.version_tag} [{self.status}]"


class RetrainingJob(models.Model):
    """
    Tracks an on-demand fine-tuning run.  FRQ-11.3, FRQ-11.4
    The job is submitted asynchronously (Celery task) and reports back here.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RUNNING = "running", "Running"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    initiated_by = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        related_name="retraining_jobs",
        limit_choices_to={"role": User.Role.ADMINISTRATOR},
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    dataset_size = models.PositiveIntegerField(default=0)
    base_model_version = models.ForeignKey(
        ModelVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="retraining_jobs",
    )
    # Filled once the job completes and produces a new ModelVersion
    result_model_version = models.ForeignKey(
        ModelVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="produced_by",
    )
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"RetrainingJob #{self.pk} [{self.status}]"
