"""analytics.serializers - read-only output shapes for statistics and history."""

from rest_framework import serializers
from apps.receiver.serializers import InspectionRecordSerializer


class OperatorStatisticsSerializer(serializers.Serializer):
    """FRQ-9.2"""

    operator_id = serializers.IntegerField()
    username = serializers.CharField()
    images_processed = serializers.IntegerField()
    defects_confirmed = serializers.IntegerField()
    avg_verification_seconds = serializers.FloatField(allow_null=True)


class OverallStatisticsSerializer(serializers.Serializer):
    """FRQ-9.3"""

    total_inspections = serializers.IntegerField()
    total_defects_detected = serializers.IntegerField()
    defects_by_type = serializers.DictField(child=serializers.IntegerField())
    operators = OperatorStatisticsSerializer(many=True)


class InspectionHistorySerializer(InspectionRecordSerializer):
    """FRQ-8.1 - extends base record with detection summary for list view."""

    defect_count = serializers.IntegerField(read_only=True)
    defect_types = serializers.ListField(child=serializers.CharField(), read_only=True)
