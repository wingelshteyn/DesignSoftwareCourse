"""
detection.services
------------------
Public API of the detection module.
FRQ-4  ML client and defect persistence
FRQ-5  InspectionRecord status update after detection

This service is the single integration point between the Django monolith
and the external ML Inference Service (Quantum 2).
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import DefectDetection, DetectedDefect
    from apps.receiver.models import InspectionRecord


class MLClientService:
    """
    HTTP client wrapper for Quantum 2 (ML Inference Service).
    Uses httpx for synchronous calls inside Celery worker context.
    FRQ-4.2
    """

    @staticmethod
    def run_inference(image_bytes: bytes, model_version: str) -> dict:
        """
        POST image bytes to ML service; return raw JSON response:
          {"defects": [{"type": "RS", "bbox": [x,y,w,h], "confidence": 0.93}, ...]}
        Raises MLServiceError on HTTP errors or timeouts.
        """
        raise NotImplementedError


class DetectionService:
    """
    Orchestrates the full detection pipeline for one InspectionRecord.
    Called exclusively from detection_task (Celery worker).
    FRQ-4.1, FRQ-4.2, FRQ-4.3, FRQ-4.4, FRQ-5
    """

    @staticmethod
    def run_detection_pipeline(record_id: int) -> "DefectDetection":
        """
        1. Load image bytes from MinIO.
        2. Pre-process image (resize / normalise).
        3. Call MLClientService.run_inference().
        4. Persist DefectDetection + DetectedDefect rows.
        5. Update InspectionRecord.status → pending (via receiver.services).
        """
        raise NotImplementedError

    @staticmethod
    def get_detection_result(inspection_id: int) -> "DefectDetection":
        """Retrieve detection result for a given InspectionRecord."""
        raise NotImplementedError


class MLServiceError(Exception):
    """Raised when the ML Inference Service returns an error or is unreachable."""
