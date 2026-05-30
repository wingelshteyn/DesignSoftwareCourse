"""
Celery task that triggers asynchronous detection after image receipt
"""

from celery import shared_task


@shared_task()
def trigger_detection_task():
    pass
