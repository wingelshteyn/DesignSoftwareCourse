"""
Authentication & role-based access (FRQ-1)
User management (administrator) (FRQ-2  )
"""

from django.contrib.auth.models import AbstractUser
from django.db import models


class Zone(models.Model):
    """control area that cameras and users belong to"""

    # name
    # description
    # created_at
    pass


class User(AbstractUser):
    """custom user model"""

    class Role(models.TextChoices):
        OPERATOR = "operator", "Operator"
        TECHNOLOGIST = "technologist", "Technologist"
        ADMINISTRATOR = "administrator", "Administrator"

    # role
    # zone = models.ForeignKey(Zone)
    # created_at
    # updated_at
    pass