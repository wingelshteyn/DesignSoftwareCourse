from dataclasses import dataclass

from apps.accounts.models import RBACPolicy
from apps.administration.models import AdministrationPolicy
from apps.detection.models import DetectionWorkflow


@dataclass(slots=True)
class VerificationWorkflow:
    """
    Verification depends on user access rules, administration rules,
    and automatic detection results.
    """

    rbac_policy: RBACPolicy
    administration_policy: AdministrationPolicy
    detection_workflow: DetectionWorkflow

    def can_start_verification(self, role: str, image_path: str) -> bool:
        if not self.administration_policy.manual_verification_enabled:
            return False
        if not self.rbac_policy.can_verify(role):
            return False
        self.detection_workflow.prepare_detection_request(image_path)
        return True
