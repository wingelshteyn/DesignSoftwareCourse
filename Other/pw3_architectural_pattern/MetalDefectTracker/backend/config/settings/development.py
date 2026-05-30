"""Development settings - debug enabled, relaxed security."""

from .base import *  # noqa: F403, F401

DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ALLOW_ALL_ORIGINS = True

# In development, store media locally instead of MinIO to simplify setup
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # noqa: F405
