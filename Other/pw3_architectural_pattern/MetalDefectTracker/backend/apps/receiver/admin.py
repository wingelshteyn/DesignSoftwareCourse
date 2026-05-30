from django.contrib import admin
from .models import Camera, InspectionRecord


@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    list_display = ["name", "zone", "status", "created_at"]
    list_filter = ["status", "zone"]


@admin.register(InspectionRecord)
class InspectionRecordAdmin(admin.ModelAdmin):
    list_display = ["pk", "camera", "status", "received_at"]
    list_filter = ["status", "camera__zone"]
    date_hierarchy = "received_at"
