"""verification.serializers"""

from rest_framework import serializers


class ManualDefectSerializer(serializers.ModelSerializer):
    pass


class DefectExclusionSerializer(serializers.ModelSerializer):
    pass


class VerificationActionSerializer(serializers.ModelSerializer):
    pass


class VerificationSubmitSerializer(serializers.Serializer):
    pass


class AuditLogSerializer(serializers.ModelSerializer):
    pass