"""administration.serializers"""

from rest_framework import serializers
from .models import CameraSettings, DefectType, ModelVersion, RetrainingJob


class CameraSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CameraSettings
        fields = [
            "id", "camera", "resolution_width", "resolution_height",
            "capture_interval_seconds", "updated_at",
        ]
        read_only_fields = ["id", "camera", "updated_at"]


class DefectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectType
        fields = ["id", "code", "label", "description", "is_builtin", "created_at"]
        read_only_fields = ["id", "is_builtin", "created_at"]


class ModelVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelVersion
        fields = [
            "id", "version_tag", "status", "confidence_threshold",
            "artifact_path", "deployed_at", "created_at",
        ]
        read_only_fields = ["id", "deployed_at", "created_at"]


class ModelVersionDeploySerializer(serializers.Serializer):
    """Payload for deploy / rollback actions."""

    version_id = serializers.IntegerField()


class ConfidenceThresholdSerializer(serializers.Serializer):
    """FRQ-11.1"""

    confidence_threshold = serializers.FloatField(min_value=0.0, max_value=1.0)


class RetrainingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetrainingJob
        fields = [
            "id", "initiated_by", "status", "dataset_size",
            "base_model_version", "result_model_version",
            "started_at", "finished_at", "created_at",
        ]
        read_only_fields = fields


class StartRetrainingSerializer(serializers.Serializer):
    """Input for POST /api/admin-panel/model/retrain/  FRQ-11.4"""

    inspection_ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)
    base_version_id = serializers.IntegerField()
