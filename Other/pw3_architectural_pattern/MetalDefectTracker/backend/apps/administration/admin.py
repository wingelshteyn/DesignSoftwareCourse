from django.contrib import admin
from .models import CameraSettings, DefectType, ModelVersion, RetrainingJob


@admin.register(CameraSettings)
class CameraSettingsAdmin(admin.ModelAdmin):
    list_display = ["camera", "resolution_width", "resolution_height", "capture_interval_seconds", "updated_at"]


@admin.register(DefectType)
class DefectTypeAdmin(admin.ModelAdmin):
    list_display = ["code", "label", "is_builtin", "created_at"]
    list_filter = ["is_builtin"]
    search_fields = ["code", "label"]


@admin.register(ModelVersion)
class ModelVersionAdmin(admin.ModelAdmin):
    list_display = ["version_tag", "status", "confidence_threshold", "deployed_at", "created_at"]
    list_filter = ["status"]


@admin.register(RetrainingJob)
class RetrainingJobAdmin(admin.ModelAdmin):
    list_display = ["pk", "initiated_by", "status", "dataset_size", "created_at"]
    list_filter = ["status"]
    readonly_fields = ["initiated_by", "status", "dataset_size", "started_at", "finished_at"]
