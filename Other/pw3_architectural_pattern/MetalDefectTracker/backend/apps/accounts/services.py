"""
accounts.services
-----------------
Public Python API of the accounts module.
Other modules MUST use these functions instead of querying accounts models directly.
This enforces the modular-monolith boundary.

FRQ-1  Authentication
FRQ-2  User management (administrator)
"""

from __future__ import annotations

from typing import Optional

from .models import User, Zone


# ---------------------------------------------------------------------------
# Zone CRUD
# ---------------------------------------------------------------------------


class ZoneService:
    """Operations on production zones / control areas.  FRQ-2.5"""

    @staticmethod
    def create_zone(name: str, description: str = "") -> Zone:
        raise NotImplementedError

    @staticmethod
    def list_zones() -> list[Zone]:
        raise NotImplementedError

    @staticmethod
    def get_zone(zone_id: int) -> Zone:
        raise NotImplementedError


# ---------------------------------------------------------------------------
# User CRUD  (administrator only - enforced at view / permission layer)
# ---------------------------------------------------------------------------


class UserService:
    """Operations on user accounts.  FRQ-2.1–FRQ-2.4"""

    @staticmethod
    def create_user(
        username: str,
        password: str,
        role: str,
        zone_id: Optional[int] = None,
    ) -> User:
        """Create a new user with the given role and zone.  FRQ-2.1, FRQ-2.2"""
        raise NotImplementedError

    @staticmethod
    def update_role(user_id: int, new_role: str) -> User:
        """Change the role of an existing user.  FRQ-2.3"""
        raise NotImplementedError

    @staticmethod
    def delete_user(user_id: int) -> None:
        """Remove a user from the system.  FRQ-2.4"""
        raise NotImplementedError

    @staticmethod
    def get_user(user_id: int) -> User:
        """Retrieve a single user by PK."""
        raise NotImplementedError

    @staticmethod
    def list_users() -> list[User]:
        """Return all users (used by analytics and admin views)."""
        raise NotImplementedError
