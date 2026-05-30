from rest_framework import serializers


class CameraSettingsSerializer(serializers.ModelSerializer):
    pass


class DefectTypeSerializer(serializers.ModelSerializer):
    pass


class ModelVersionSerializer(serializers.ModelSerializer):
    pass


class ModelVersionDeploySerializer(serializers.Serializer):
    pass


class ConfidenceThresholdSerializer(serializers.Serializer):
    pass


class RetrainingJobSerializer(serializers.ModelSerializer):
    pass


class StartRetrainingSerializer(serializers.Serializer):
    pass
