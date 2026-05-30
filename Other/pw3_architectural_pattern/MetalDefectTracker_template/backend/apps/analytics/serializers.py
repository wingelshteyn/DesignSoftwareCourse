"""read-only output shapes for statistics and history"""

from rest_framework import serializers
from apps.receiver.serializers import InspectionRecordSerializer


class OperatorStatisticsSerializer(serializers.Serializer):
    pass


class OverallStatisticsSerializer(serializers.Serializer):
    pass


class InspectionHistorySerializer(InspectionRecordSerializer):
    pass
