"""
receiver.models
---------------
FRQ-3  Image ingestion and storage
FRQ-5  Inspection record status lifecycle

Depends on:
  accounts.Zone  (ForeignKey: Camera -> Zone)
"""

from django.db import models
from apps.accounts.models import Zone


class Camera(models.Model):
    """
    Represents a physical camera on a production line.
    Settings (resolution, interval) live in administration.CameraSettings.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    name = models.CharField(max_length=100)
    zone = models.ForeignKey(
        Zone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="cameras",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class InspectionRecord(models.Model):
    """
    Central entity tying together an image, its detection result,
    and all subsequent operator actions.  FRQ-3.3, FRQ-5.1
    """

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"        # image saved, detection not yet started
        PENDING = "pending", "Pending"    # detection done, awaiting operator
        ACCEPTED = "accepted", "Accepted"  # operator: product OK
        REJECTED = "rejected", "Rejected"  # operator: product is defective

    camera = models.ForeignKey(
        Camera,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inspections",
    )
    # MinIO object key - actual file lives in S3-compatible storage, not in DB.
    # Django FileField / ImageField via django-storages points to MinIO.
    image = models.ImageField(
        upload_to="inspections/%Y/%m/%d/",
        help_text="Stored in MinIO via django-storages.",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.QUEUED
    )
    received_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-received_at"]

    def __str__(self) -> str:
        return f"InspectionRecord #{self.pk} [{self.status}]"
