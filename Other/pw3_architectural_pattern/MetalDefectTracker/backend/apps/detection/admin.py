from django.contrib import admin
from .models import DefectDetection, DetectedDefect


class DetectedDefectInline(admin.TabularInline):
    model = DetectedDefect
    extra = 0
    readonly_fields = ["defect_type", "bbox_x", "bbox_y", "bbox_w", "bbox_h", "confidence", "is_active"]


@admin.register(DefectDetection)
class DefectDetectionAdmin(admin.ModelAdmin):
    list_display = ["pk", "inspection", "ml_model_version", "processed_at"]
    inlines = [DetectedDefectInline]
