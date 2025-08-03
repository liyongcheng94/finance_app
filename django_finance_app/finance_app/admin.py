from django.contrib import admin
from .models import FinanceRecord, ProcessingLog


@admin.register(FinanceRecord)
class FinanceRecordAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "filename",
        "upload_time",
        "status",
        "total_records",
        "processing_time",
    ]
    list_filter = ["status", "upload_time", "user"]
    search_fields = ["filename", "user__username"]
    readonly_fields = ["upload_time", "file_size", "output_file_size"]
    date_hierarchy = "upload_time"
    ordering = ["-upload_time"]

    fieldsets = (
        ("基本信息", {"fields": ("user", "filename", "file_path", "upload_time")}),
        (
            "处理状态",
            {"fields": ("status", "error_message", "total_records", "processing_time")},
        ),
        ("输出结果", {"fields": ("output_file_path", "output_filename")}),
    )


@admin.register(ProcessingLog)
class ProcessingLogAdmin(admin.ModelAdmin):
    list_display = ["id", "record", "timestamp", "level", "message_preview"]
    list_filter = ["level", "timestamp"]
    search_fields = ["message", "record__filename"]
    readonly_fields = ["timestamp"]
    date_hierarchy = "timestamp"
    ordering = ["-timestamp"]

    def message_preview(self, obj):
        return obj.message[:100] + "..." if len(obj.message) > 100 else obj.message

    message_preview.short_description = "消息预览"
