"""
Image ingestion and storage
Inspection record status lifecycle
"""

from django.db import models
from apps.accounts.models import Zone


class Camera(models.Model):
    """
    Represents a physical camera on a production line
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    # name
    # zone = models.ForeignKey(Zone)
    # status


class InspectionRecord(models.Model):
    """
    Central entity tying together an image, its detection result
    """

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"        # image saved, detection not yet started
        PENDING = "pending", "Pending"    # detection done, awaiting operator
        ACCEPTED = "accepted", "Accepted"  # operator: product OK
        REJECTED = "rejected", "Rejected"  # operator: product is defective

    # camera = models.ForeignKey(Camera)
    # image
    # status
