"""receiver.serializers"""

from rest_framework import serializers
from .models import Camera, InspectionRecord


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ["id", "name", "zone", "status", "created_at"]
        read_only_fields = ["id", "created_at"]


class InspectionRecordSerializer(serializers.ModelSerializer):
    camera = CameraSerializer(read_only=True)

    class Meta:
        model = InspectionRecord
        fields = ["id", "camera", "image", "status", "received_at", "updated_at"]
        read_only_fields = ["id", "status", "received_at", "updated_at"]


class ImageUploadSerializer(serializers.Serializer):
    """Used for the camera → API POST endpoint.  FRQ-3.1"""

    camera_id = serializers.IntegerField()
    image = serializers.ImageField()
