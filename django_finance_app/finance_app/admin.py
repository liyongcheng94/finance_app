from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import FinanceRecord, ProcessingLog, UserProfile


class UserProfileInline(admin.StackedInline):
    """用户扩展信息内联编辑"""

    model = UserProfile
    can_delete = False
    verbose_name_plural = "用户扩展信息"
    fields = ("display_name",)


class CustomUserAdmin(UserAdmin):
    """自定义用户管理"""

    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户扩展信息管理"""

    list_display = ["user", "display_name", "created_at", "updated_at"]
    list_filter = ["created_at", "updated_at"]
    search_fields = ["user__username", "display_name"]
    readonly_fields = ["created_at", "updated_at"]


# 重新注册User模型
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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
