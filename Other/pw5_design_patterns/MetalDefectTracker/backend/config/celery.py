"""
Celery application for MetalDefectTracker (Quantum 1).

Workers run from the same Docker image as Django and share all models/DB.
The broker is Redis; results are also stored in Redis.

Tasks registered here:
  - apps.detection.tasks.detection_task   (ML inference pipeline)
"""

import os
from celery import Celery

# Point to the base Django settings by default; override in production via env var
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("mdt")

# Load Celery configuration from Django settings (CELERY_* keys)
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()
