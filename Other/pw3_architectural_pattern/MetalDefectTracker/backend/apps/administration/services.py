"""
administration.services
-----------------------
Public API of the administration module.
FRQ-10  Camera configuration
FRQ-11  Defect type catalog + model fine-tuning
FRQ-12  Model version management and rollback
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import CameraSettings, DefectType, ModelVersion, RetrainingJob


class CameraConfigService:
    """Camera settings management.  FRQ-10.1–FRQ-10.3"""

    @staticmethod
    def get_or_create_settings(camera_id: int) -> "CameraSettings":
        raise NotImplementedError

    @staticmethod
    def update_settings(
        camera_id: int,
        resolution_width: int | None = None,
        resolution_height: int | None = None,
        capture_interval_seconds: float | None = None,
    ) -> "CameraSettings":
        raise NotImplementedError


class DefectTypeService:
    """Defect catalog management.  FRQ-11.2"""

    @staticmethod
    def list_defect_types() -> list["DefectType"]:
        raise NotImplementedError

    @staticmethod
    def add_defect_type(code: str, label: str, description: str = "") -> "DefectType":
        """Add a new custom defect type to the catalog.  FRQ-11.2"""
        raise NotImplementedError

    @staticmethod
    def get_other_defect_images() -> list[dict]:
        """
        Return ManualDefects marked as 'other' grouped for reclassification.
        FRQ-11.3
        """
        raise NotImplementedError


class ModelVersionService:
    """ML model version lifecycle.  FRQ-12.1, FRQ-12.2"""

    @staticmethod
    def list_versions() -> list["ModelVersion"]:
        raise NotImplementedError

    @staticmethod
    def get_active_version() -> "ModelVersion":
        raise NotImplementedError

    @staticmethod
    def deploy_version(version_id: int) -> "ModelVersion":
        """
        Set version as ACTIVE, previous active → ROLLBACK.
        Kubernetes rolling-update is triggered externally by the K8s operator
        reading the active version artifact_path.  FRQ-12.2
        """
        raise NotImplementedError

    @staticmethod
    def rollback(target_version_id: int) -> "ModelVersion":
        """Reactivate a ROLLBACK version.  FRQ-12.2, NFRQ-3.1"""
        raise NotImplementedError

    @staticmethod
    def set_confidence_threshold(version_id: int, threshold: float) -> "ModelVersion":
        """Update the confidence threshold for a staging/active version.  FRQ-11.1"""
        raise NotImplementedError


class RetrainingService:
    """Model fine-tuning workflow.  FRQ-11.3, FRQ-11.4"""

    @staticmethod
    def initiate_retraining(
        initiated_by_id: int,
        inspection_ids: list[int],
        base_version_id: int,
    ) -> "RetrainingJob":
        """
        Creates a RetrainingJob and enqueues a Celery task that:
          1. Collects labelled image data for given inspections.
          2. Triggers fine-tuning on the ML service or a training pipeline.
          3. Registers resulting artifact as a new ModelVersion (status=staging).
        FRQ-11.4
        """
        raise NotImplementedError

    @staticmethod
    def get_job(job_id: int) -> "RetrainingJob":
        raise NotImplementedError
