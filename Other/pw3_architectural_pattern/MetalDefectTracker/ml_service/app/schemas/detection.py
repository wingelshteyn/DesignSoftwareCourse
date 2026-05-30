"""
ml_service.app.schemas.detection
---------------------------------
Pydantic schemas for the detection request/response contract.

This contract is consumed by:
  - detection.services.MLClientService  (Quantum 1 caller)
  - ML Inference Service API endpoints   (Quantum 2 provider)
"""

from __future__ import annotations
from typing import Annotated
from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Bounding box in pixel coordinates (top-left origin)."""

    x: float = Field(..., description="Top-left x coordinate")
    y: float = Field(..., description="Top-left y coordinate")
    w: float = Field(..., description="Width of the box")
    h: float = Field(..., description="Height of the box")


class DetectedDefectSchema(BaseModel):
    """Single detected defect returned by the model."""

    defect_type: str = Field(
        ...,
        description=(
            "Defect class code: RS, Pa, Cr, PS, In, Sc, or 'other'. "
            "Must match administration.DefectType.code values."
        ),
        examples=["RS", "Cr", "other"],
    )
    bbox: BoundingBox
    confidence: Annotated[float, Field(ge=0.0, le=1.0)] = Field(
        ..., description="Model confidence score [0, 1]."
    )


class DetectionRequest(BaseModel):
    """
    Optional per-request override for confidence threshold.
    The image itself is sent as multipart/form-data, not in this body.
    """

    confidence_threshold: Annotated[float, Field(ge=0.0, le=1.0)] | None = Field(
        default=None,
        description="Override the service-level confidence threshold for this request.",
    )


class DetectionResponse(BaseModel):
    """Response envelope returned by POST /detect."""

    model_version: str = Field(..., description="Version tag of the model that produced this result.")
    defects: list[DetectedDefectSchema] = Field(
        default_factory=list,
        description="List of detected defects. Empty list = no defects found.",
    )
    inference_time_ms: float = Field(..., description="Inference wall-clock time in milliseconds.")


class HealthResponse(BaseModel):
    status: str = "ok"
    model_version: str
    model_loaded: bool
