"""
accounts.permissions
--------------------
Custom DRF permission classes based on the User.role field.
Used across all apps - imported as needed.

FRQ-1.2  Role-based access control
NFRQ-1.1  Secure role enforcement
"""

from rest_framework.permissions import BasePermission
from .models import User


class IsAdministrator(BasePermission):
    """Allow access only to users with the ADMINISTRATOR role."""

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMINISTRATOR
        )


class IsTechnologist(BasePermission):
    """Allow access only to users with the TECHNOLOGIST role."""

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.TECHNOLOGIST
        )


class IsOperator(BasePermission):
    """Allow access only to users with the OPERATOR role."""

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.OPERATOR
        )


class IsAdministratorOrTechnologist(BasePermission):
    """Allow TECHNOLOGIST or ADMINISTRATOR (analytics, reports)."""

    def has_permission(self, request, view) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in (
            User.Role.ADMINISTRATOR,
            User.Role.TECHNOLOGIST,
        )


class IsAdministratorOrOperator(BasePermission):
    """Allow OPERATOR or ADMINISTRATOR (shared verification/history views)."""

    def has_permission(self, request, view) -> bool:
        if not (request.user and request.user.is_authenticated):
            return False
        return request.user.role in (
            User.Role.ADMINISTRATOR,
            User.Role.OPERATOR,
        )
