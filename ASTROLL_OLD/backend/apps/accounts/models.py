from dataclasses import dataclass
from enum import Enum


class UserRole(str, Enum):
    PLAYER = "player"
    MASTER = "master"
    ADMIN = "admin"


@dataclass(frozen=True)
class UserProfile:
    user_id: int
    login: str
    nickname: str
    role: UserRole = UserRole.PLAYER


class RBACPolicy:
    """Stable access policy reused by other monolith modules."""

    def can_administer(self, profile: UserProfile) -> bool:
        return profile.role == UserRole.ADMIN

    def can_host_room(self, profile: UserProfile) -> bool:
        return profile.role in {UserRole.MASTER, UserRole.ADMIN}
