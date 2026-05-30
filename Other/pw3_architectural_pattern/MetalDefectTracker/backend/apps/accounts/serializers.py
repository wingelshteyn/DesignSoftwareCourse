"""
accounts.serializers
"""

from rest_framework import serializers
from .models import User, Zone


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zone
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    zone = ZoneSerializer(read_only=True)
    zone_id = serializers.PrimaryKeyRelatedField(
        queryset=Zone.objects.all(), source="zone", write_only=True, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "role", "zone", "zone_id", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class UserCreateSerializer(serializers.ModelSerializer):
    """Used by administrator to create new accounts.  FRQ-2.1, FRQ-2.2"""

    password = serializers.CharField(write_only=True, min_length=8)
    zone_id = serializers.PrimaryKeyRelatedField(
        queryset=Zone.objects.all(), source="zone", allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "zone_id"]


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    """Used by administrator to change a user's role.  FRQ-2.3"""

    class Meta:
        model = User
        fields = ["role"]
