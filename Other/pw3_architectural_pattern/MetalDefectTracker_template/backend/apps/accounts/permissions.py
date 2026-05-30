"""
Custom DRF permission classes based on the User.role field
"""

from rest_framework.permissions import BasePermission
from .models import User


class IsAdministrator(BasePermission):
    """Allow access only to users with the ADMINISTRATOR role"""

    def has_permission(self, request, view) -> bool:
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == User.Role.ADMINISTRATOR
        )


class IsTechnologist(BasePermission):
    """TECHNOLOGIST"""

    def has_permission(self) -> bool:
        pass


class IsOperator(BasePermission):
    """OPERATOR"""

    def has_permission(self) -> bool:
        pass


class IsAdministratorOrTechnologist(BasePermission):
    """TECHNOLOGIST or ADMINISTRATOR"""

    def has_permission(self) -> bool:
        pass


class IsAdministratorOrOperator(BasePermission):
    """OPERATOR or ADMINISTRATOR"""

    def has_permission(self) -> bool:
        pass
