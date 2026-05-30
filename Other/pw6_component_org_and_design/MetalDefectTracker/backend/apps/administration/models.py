from dataclasses import dataclass

from apps.accounts.models import RBACPolicy


@dataclass(slots=True)
class AdministrationPolicy:
    """
    Administrative settings used by other components.
    Depends on Accounts because management is constrained by RBAC rules.
    """

    rbac_policy: RBACPolicy
    camera_resolution: str = "1920x1080"
    capture_interval_seconds: int = 5
    detection_threshold: float = 0.5
    manual_verification_enabled: bool = True

    def can_manage_configuration(self, role: str) -> bool:
        return self.rbac_policy.can_manage_system(role)
