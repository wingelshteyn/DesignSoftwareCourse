from dataclasses import dataclass

from apps.administration.models import AdministrationPolicy
from apps.receiver.models import ImageReceptionService


@dataclass(slots=True)
class DetectionWorkflow:
    """
    Uses received image data together with administrative settings
    to prepare a detection request for the core detection logic.
    """

    administration_policy: AdministrationPolicy
    reception_service: ImageReceptionService

    def prepare_detection_request(self, image_path: str) -> dict[str, object]:
        received_image = self.reception_service.receive(image_path)
        return {
            "image_path": received_image["image_path"],
            "resolution": received_image["resolution"],
            "threshold": self.administration_policy.detection_threshold,
        }
