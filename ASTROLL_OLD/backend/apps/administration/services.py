from dataclasses import dataclass

from apps.accounts.models import RBACPolicy, UserProfile


@dataclass(frozen=True)
class RuntimeSettings:
    max_room_members: int = 8
    autosave_interval_seconds: int = 30
    readonly_by_default: bool = False


class AdministrationPolicy:
    def __init__(self, rbac: RBACPolicy) -> None:
        self._rbac = rbac

    def can_change_runtime_settings(self, profile: UserProfile) -> bool:
        return self._rbac.can_administer(profile)
