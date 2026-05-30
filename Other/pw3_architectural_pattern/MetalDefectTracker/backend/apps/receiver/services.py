"""
receiver.services
-----------------
Public API of the receiver module.
FRQ-3  Image ingestion and InspectionRecord lifecycle.

The service layer is the ONLY way other modules (detection, analytics)
should interact with receiver data - no direct model imports from outside.
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.core.files import File
    from .models import Camera, InspectionRecord


class ImageReceiverService:
    """Handles incoming images from cameras.  FRQ-3.1–FRQ-3.3"""

    @staticmethod
    def receive_image(camera_id: int, image_file: "File") -> "InspectionRecord":
        """
        Persist image to MinIO and create an InspectionRecord (status=queued).
        Enqueues detection_task via Celery immediately after.
        Returns 202-ready record so the camera endpoint can respond fast.
        """
        raise NotImplementedError

    @staticmethod
    def get_inspection(record_id: int) -> "InspectionRecord":
        raise NotImplementedError

    @staticmethod
    def update_status(record_id: int, new_status: str) -> "InspectionRecord":
        """
        Called by detection.tasks and verification.services to advance status.
        Allowed transitions: queued→pending, pending→accepted/rejected
        """
        raise NotImplementedError

    @staticmethod
    def list_inspections(
        zone_id: int | None = None,
        camera_id: int | None = None,
    ) -> list["InspectionRecord"]:
        """Return all InspectionRecords, optionally scoped to a zone/camera."""
        raise NotImplementedError
