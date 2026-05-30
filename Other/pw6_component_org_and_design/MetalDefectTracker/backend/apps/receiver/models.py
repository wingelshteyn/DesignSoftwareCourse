from dataclasses import dataclass

from apps.administration.models import AdministrationPolicy


@dataclass(slots=True)
class ImageReceptionService:
    """
    Receives image metadata and uses Administration settings.
    Represents the Receiver component in the component dependency graph.
    """

    administration_policy: AdministrationPolicy

    def receive(self, image_path: str) -> dict[str, str | int]:
        return {
            "image_path": image_path,
            "resolution": self.administration_policy.camera_resolution,
            "capture_interval_seconds": self.administration_policy.capture_interval_seconds,
        }
