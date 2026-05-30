from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    PLAYER = "player"
    MASTER = "master"
    ADMIN = "admin"


@dataclass(frozen=True)
class User:
    user_id: int
    login: str
    nickname: str
    role: Role


class AuthorizationPolicy:
    def can_administer(self, user: User) -> bool:
        return user.role == Role.ADMIN

    def can_host(self, user: User) -> bool:
        return user.role in {Role.MASTER, Role.ADMIN}
