"""verification.serializers"""

from rest_framework import serializers
from .models import AuditLog, DefectExclusion, ManualDefect, VerificationAction


class ManualDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManualDefect
        fields = ["id", "defect_type", "bbox_x", "bbox_y", "bbox_w", "bbox_h", "created_at"]
        read_only_fields = ["id", "created_at"]


class DefectExclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectExclusion
        fields = ["id", "defect", "excluded_at"]
        read_only_fields = ["id", "excluded_at"]


class VerificationActionSerializer(serializers.ModelSerializer):
    manual_defects = ManualDefectSerializer(many=True, read_only=True)
    exclusions = DefectExclusionSerializer(many=True, read_only=True)

    class Meta:
        model = VerificationAction
        fields = [
            "id", "inspection", "operator", "decision",
            "time_to_verify", "verified_at",
            "manual_defects", "exclusions",
        ]
        read_only_fields = ["id", "operator", "time_to_verify", "verified_at"]


class VerificationSubmitSerializer(serializers.Serializer):
    """Input payload for POST /api/verification/<inspection_pk>/submit/"""

    decision = serializers.ChoiceField(choices=VerificationAction.Decision.choices)
    excluded_defect_ids = serializers.ListField(
        child=serializers.IntegerField(), required=False, default=list
    )
    manual_defects = ManualDefectSerializer(many=True, required=False, default=list)


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ["id", "user", "inspection", "action_type", "details", "timestamp"]
        read_only_fields = fields
