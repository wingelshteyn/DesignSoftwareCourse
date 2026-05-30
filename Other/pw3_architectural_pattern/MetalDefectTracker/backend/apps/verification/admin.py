from django.contrib import admin
from .models import AuditLog, DefectExclusion, ManualDefect, VerificationAction


class ManualDefectInline(admin.TabularInline):
    model = ManualDefect
    extra = 0


class DefectExclusionInline(admin.TabularInline):
    model = DefectExclusion
    extra = 0


@admin.register(VerificationAction)
class VerificationActionAdmin(admin.ModelAdmin):
    list_display = ["pk", "inspection", "operator", "decision", "verified_at"]
    list_filter = ["decision"]
    inlines = [ManualDefectInline, DefectExclusionInline]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["pk", "user", "inspection", "action_type", "timestamp"]
    list_filter = ["action_type"]
    readonly_fields = ["user", "inspection", "action_type", "details", "timestamp"]
