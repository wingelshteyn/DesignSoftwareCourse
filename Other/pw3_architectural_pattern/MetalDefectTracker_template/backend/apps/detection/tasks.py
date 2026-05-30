"""
detection.tasks
---------------
Celery tasks for asynchronous ML inference pipeline.
FRQ-4  Automatic defect detection
FRQ-5  Status lifecycle management
"""

from celery import shared_task


@shared_task()
def detection_task():
    """
    Main detection pipeline task
    """
    from .services import DetectionService, MLServiceError
    pass
