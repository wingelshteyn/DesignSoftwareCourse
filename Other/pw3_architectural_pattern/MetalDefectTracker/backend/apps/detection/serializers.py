"""detection.serializers"""

from rest_framework import serializers
from .models import DefectDetection, DetectedDefect


class DetectedDefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedDefect
        fields = [
            "id", "defect_type", "bbox_x", "bbox_y", "bbox_w", "bbox_h",
            "confidence", "is_active",
        ]
        read_only_fields = ["id"]


class DefectDetectionSerializer(serializers.ModelSerializer):
    defects = DetectedDefectSerializer(many=True, read_only=True)

    class Meta:
        model = DefectDetection
        fields = ["id", "inspection", "ml_model_version", "processed_at", "defects"]
        read_only_fields = ["id", "processed_at"]
