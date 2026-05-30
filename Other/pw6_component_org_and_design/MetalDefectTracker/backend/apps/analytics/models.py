from dataclasses import dataclass

from apps.accounts.models import RBACPolicy
from apps.receiver.models import ImageReceptionService
from apps.verification.models import VerificationWorkflow


@dataclass(slots=True)
class AnalyticsReportService:
    """
    Analytics is the outer consumer of access rules,
    received image history, and verification results.
    """

    rbac_policy: RBACPolicy
    reception_service: ImageReceptionService
    verification_workflow: VerificationWorkflow

    def build_summary(self, role: str, image_path: str) -> dict[str, object]:
        if not self.rbac_policy.can_view_analytics(role):
            raise PermissionError("Analytics access denied.")

        received_image = self.reception_service.receive(image_path)
        verification_available = self.verification_workflow.can_start_verification(
            role="operator",
            image_path=image_path,
        )
        return {
            "received_resolution": received_image["resolution"],
            "verification_available": verification_available,
            "requested_by": role,
        }
