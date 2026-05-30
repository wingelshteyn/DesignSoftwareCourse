"""
ml_service.app.config
---------------------
Environment-based configuration for the ML Inference Service.
Values are read from environment variables or a .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Model artifact location (local path or MinIO-mounted path)
    model_path: str = "models/current/model.onnx"

    # Default confidence threshold (can be overridden per-request or via env)
    confidence_threshold: float = 0.5

    # Service metadata
    model_version: str = "unknown"
    service_host: str = "0.0.0.0"
    service_port: int = 8001

    # Input image size expected by the model (width, height)
    input_width: int = 640
    input_height: int = 640


settings = Settings()
