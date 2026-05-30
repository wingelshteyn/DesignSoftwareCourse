"""
ml_service.app.main
--------------------
FastAPI application entry point for Quantum 2 (ML Inference Service).

Endpoints:
  POST /detect   - run inference on an uploaded image
  GET  /health   - liveness probe for Kubernetes

The service is deployed as an independent component and scales via
Kubernetes HPA. Django monolith (Quantum 1) communicates with it
exclusively through these HTTP endpoints.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status

from .config import settings
from .model.inference import InferenceService
from .model.loader import model_loader
from .schemas.detection import DetectionResponse, HealthResponse

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Lifespan: load model at startup, unload at shutdown
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the ML model once on startup."""
    try:
        model_loader.load(
            model_path=settings.model_path,
            version=settings.model_version,
        )
    except FileNotFoundError:
        # Service starts even without the model file (useful in staging / CI).
        # Health endpoint will return model_loaded=False.
        logger.warning(
            "Model artifact not found at '%s'. Service running without model.",
            settings.model_path,
        )
    yield
    model_loader.unload()


# ---------------------------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="MDT ML Inference Service",
    description=(
        "Quantum 2 of the MetalDefectTracker architecture. "
        "Accepts metal sheet images and returns defect detections."
    ),
    version=settings.model_version,
    lifespan=lifespan,
)

_inference_service = InferenceService(model_loader)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@app.get("/health", response_model=HealthResponse, tags=["ops"])
async def health_check() -> HealthResponse:
    """
    Kubernetes liveness / readiness probe.
    Returns 200 even if model is not loaded (readiness probe should check model_loaded).
    """
    return HealthResponse(
        status="ok",
        model_version=model_loader.version,
        model_loaded=model_loader.is_loaded,
    )


@app.post(
    "/detect",
    response_model=DetectionResponse,
    tags=["inference"],
    summary="Run defect detection on a metal sheet image",
)
async def detect_defects(
    image: UploadFile = File(..., description="Metal sheet image (JPEG / PNG)."),
    confidence_threshold: float | None = Form(
        default=None,
        ge=0.0,
        le=1.0,
        description="Optional per-request confidence threshold override.",
    ),
) -> DetectionResponse:
    """
    Accepts a metal sheet image via multipart/form-data.
    Returns a list of detected defects with type, bounding box, and confidence.

    Called exclusively by Quantum 1 (Django detection.tasks.detection_task)
    running inside a Celery worker.  FRQ-4.2
    """
    if not model_loader.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Service is not ready.",
        )

    image_bytes = await image.read()
    threshold = confidence_threshold if confidence_threshold is not None else settings.confidence_threshold

    try:
        result = _inference_service.run(
            image_bytes=image_bytes,
            confidence_threshold=threshold,
            input_width=settings.input_width,
            input_height=settings.input_height,
        )
    except NotImplementedError:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="Inference pipeline not yet implemented.",
        )

    return result
