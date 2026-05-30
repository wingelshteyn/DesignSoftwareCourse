"""
accounts.models
---------------
FRQ-1  Authentication & role-based access
FRQ-2  User management (administrator)

Inter-module usage:
  - receiver  imports Zone (ForeignKey on Camera)
  - verification imports User (ForeignKey on VerificationAction, AuditLog)
  - analytics  imports User (statistics aggregation)
  - administration imports User (ForeignKey on RetrainingJob)
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Zone(models.Model):
    """Production zone / control area that cameras and users belong to. FRQ-2.5"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds role + zone assignment to standard auth fields.  FRQ-1.2, FRQ-1.3
    """

    class Role(models.TextChoices):
        OPERATOR = "operator", "Operator"
        TECHNOLOGIST = "technologist", "Technologist"
        ADMINISTRATOR = "administrator", "Administrator"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OPERATOR,
    )
    zone = models.ForeignKey(
        Zone,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="users",
        help_text="Zone / area of responsibility this user is assigned to.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"

    # ------------------------------------------------------------------
    # Convenience role-check properties
    # ------------------------------------------------------------------

    @property
    def is_operator(self) -> bool:
        return self.role == self.Role.OPERATOR

    @property
    def is_technologist(self) -> bool:
        return self.role == self.Role.TECHNOLOGIST

    @property
    def is_administrator(self) -> bool:
        return self.role == self.Role.ADMINISTRATOR
