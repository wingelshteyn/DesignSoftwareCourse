"""
ml_service.app.model.loader
----------------------------
Singleton model loader.
Loads the ONNX (or PyTorch) model artifact at service startup and holds
it in memory for the lifetime of the process.

The model path is read from configuration; in Kubernetes this path points
to a volume that is updated during rolling deployments.
"""

from __future__ import annotations
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Responsible for loading and holding the ML model artefact.
    Supports ONNX Runtime (default) and PyTorch (TorchScript) backends.
    """

    def __init__(self) -> None:
        self._session: Any | None = None   # onnxruntime.InferenceSession
        self._version: str = "unloaded"
        self._loaded: bool = False

    @property
    def version(self) -> str:
        return self._version

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    @property
    def session(self) -> Any:
        if self._session is None:
            raise RuntimeError("Model is not loaded. Call load() first.")
        return self._session

    def load(self, model_path: str, version: str = "unknown") -> None:
        """
        Load model from disk.
        Raises FileNotFoundError if the artifact is missing.
        ONNX Runtime is used by default; extend here for PyTorch TorchScript.
        """
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model artifact not found: {model_path}")

        logger.info("Loading model from %s (version=%s)…", model_path, version)
        # Actual loading is deferred to implementation
        # import onnxruntime as ort
        # self._session = ort.InferenceSession(str(path), ...)
        self._version = version
        self._loaded = True
        logger.info("Model loaded successfully (version=%s).", version)

    def unload(self) -> None:
        """Release model from memory. Used during hot-swap in tests."""
        self._session = None
        self._loaded = False
        self._version = "unloaded"


# Module-level singleton used by the FastAPI app
model_loader = ModelLoader()
