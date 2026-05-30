"""
FastAPI application entry point for ML Inference Service.
"""

from fastapi import FastAPI

from .config import settings
from .model.inference import InferenceService
from .model.loader import model_loader


app = FastAPI()

_inference_service = InferenceService(model_loader)


@app.get("/health")
async def health_check():
    # run inference on an uploaded image
    pass


@app.post("/detect")
async def detect_defects(image):
    # liveness probe for Kubernetes
    pass
