"""
ml_service.app.model.inference
--------------------------------
Pre-processing and inference pipeline.

Responsibilities:
  1. Decode raw image bytes to a PIL Image.
  2. Pre-process the image to match the model's expected input
     (resize, normalise, convert to numpy array / tensor).
  3. Run the ONNX session and parse raw outputs into DetectedDefect objects.
  4. Apply confidence threshold filtering.
"""

from __future__ import annotations
import time
import logging
from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.detection import DetectedDefectSchema, DetectionResponse
    from app.model.loader import ModelLoader

logger = logging.getLogger(__name__)

# Mapping from model output class index → defect type code
CLASS_INDEX_TO_TYPE: dict[int, str] = {
    0: "RS",    # Rolled-in Scale
    1: "Pa",    # Patches
    2: "Cr",    # Crazing
    3: "PS",    # Pitted Surface
    4: "In",    # Inclusion
    5: "Sc",    # Scratches
    6: "other",
}


class InferenceService:
    """
    Wraps the model session with pre/post-processing.
    Stateless - all state lives in ModelLoader.
    """

    def __init__(self, loader: "ModelLoader") -> None:
        self._loader = loader

    def _preprocess(self, image_bytes: bytes, input_width: int, input_height: int):
        """
        Convert raw bytes → normalised numpy array matching model input.
        Shape: (1, 3, H, W), dtype float32, values in [0, 1].
        """
        # from PIL import Image
        # import numpy as np
        # img = Image.open(BytesIO(image_bytes)).convert("RGB")
        # img = img.resize((input_width, input_height))
        # arr = np.array(img, dtype=np.float32) / 255.0
        # return arr.transpose(2, 0, 1)[np.newaxis]  # NCHW
        raise NotImplementedError

    def _postprocess(
        self,
        raw_output,
        confidence_threshold: float,
    ) -> list["DetectedDefectSchema"]:
        """
        Convert raw model output tensors → list of DetectedDefectSchema.
        Applies confidence threshold and NMS (non-maximum suppression) if needed.
        """
        # Iterate over detections, build DetectedDefectSchema objects
        raise NotImplementedError

    def run(
        self,
        image_bytes: bytes,
        confidence_threshold: float,
        input_width: int,
        input_height: int,
    ) -> "DetectionResponse":
        """
        Full inference pipeline.  Called by the FastAPI /detect endpoint.
        Returns a DetectionResponse with detected defects and timing info.
        """
        from app.schemas.detection import DetectionResponse

        start = time.perf_counter()
        input_tensor = self._preprocess(image_bytes, input_width, input_height)
        raw_output = self._loader.session.run(None, {"images": input_tensor})
        defects = self._postprocess(raw_output, confidence_threshold)
        elapsed_ms = (time.perf_counter() - start) * 1000

        return DetectionResponse(
            model_version=self._loader.version,
            defects=defects,
            inference_time_ms=round(elapsed_ms, 2),
        )
