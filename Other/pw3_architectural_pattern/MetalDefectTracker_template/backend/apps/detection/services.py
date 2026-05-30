"""
Public API of the detection module
"""

from __future__ import annotations


class MLClientService:
    """
    HTTP client wrapper for ML Inference Service
    """

    def run_inference():
        pass


class DetectionService:
    """
    Orchestrates the full detection pipeline for one InspectionRecord
    """

    def run_detection_pipeline():
        pass

    def get_detection_result():
        pass


class MLServiceError(Exception):
    """Raised when the ML Inference Service returns an error or is unreachable."""
