"""
receiver.tasks
--------------
Celery task that triggers asynchronous detection after image receipt.

This module defines the Celery task entry point only.
Actual ML invocation logic lives in detection.tasks to respect the
boundary between modules.
"""

from celery import shared_task


@shared_task(bind=True, name="receiver.trigger_detection")
def trigger_detection_task(self, inspection_record_id: int) -> None:
    """
    Thin relay task: called by ImageReceiverService right after image is saved.
    Delegates to detection.tasks.detection_task to perform the ML inference.

    Using a relay keeps receiver decoupled from detection at the task level -
    receiver only knows the record ID, not the detection pipeline details.
    """
    from apps.detection.tasks import detection_task  # late import avoids circular deps

    detection_task.delay(inspection_record_id)
