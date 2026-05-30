"""
detection.tasks
---------------
Celery tasks for asynchronous ML inference pipeline.
FRQ-4  Automatic defect detection
FRQ-5  Status lifecycle management
"""

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    name="detection.detection_task",
    max_retries=3,
    default_retry_delay=10,  # seconds
)
def detection_task(self, inspection_record_id: int) -> None:
    """
    Main detection pipeline task.

    Flow (see ADR §Поток обработки изображения):
      1. Read image bytes from MinIO.
      2. POST to ML Inference Service (Quantum 2) via DetectionService.
      3. Persist results → DetectedDefect rows.
      4. Update InspectionRecord.status = 'pending'.

    On ML service failure the task is retried up to max_retries times.
    """
    from .services import DetectionService, MLServiceError

    try:
        DetectionService.run_detection_pipeline(inspection_record_id)
    except MLServiceError as exc:
        logger.warning(
            "ML service error for inspection #%s: %s. Retrying…",
            inspection_record_id,
            exc,
        )
        raise self.retry(exc=exc)
