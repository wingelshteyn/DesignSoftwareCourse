"""
Public Python API of the accounts module
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# Zone CRUD
# ---------------------------------------------------------------------------


class ZoneService:
    """Operations on control areas"""

    def create_zone():
        pass

    def list_zones():
        pass

    def get_zone():
        pass


# ---------------------------------------------------------------------------
# User CRUD  (administrator only)
# ---------------------------------------------------------------------------


class UserService:
    """Operations on user accounts"""

    def create_user():
        pass

    def update_role():
        pass

    def delete_user():
        pass

    def get_user():
        pass

    def list_users():
        pass
