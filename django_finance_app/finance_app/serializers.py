from rest_framework import serializers
from .models import FinanceRecord, ProcessingLog


class FinanceRecordSerializer(serializers.ModelSerializer):
    """财务记录序列化器"""

    file_size_display = serializers.SerializerMethodField()
    output_file_size_display = serializers.SerializerMethodField()
    process_type_display = serializers.CharField(
        source="get_process_type_display", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    upload_time_display = serializers.DateTimeField(
        source="upload_time", format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = FinanceRecord
        fields = [
            "id",
            "filename",
            "file_path",
            "process_type",
            "process_type_display",
            "upload_time",
            "upload_time_display",
            "status",
            "status_display",
            "error_message",
            "output_file_path",
            "output_filename",
            "total_records",
            "processing_time",
            "file_size_display",
            "output_file_size_display",
        ]
        read_only_fields = [
            "id",
            "upload_time",
            "status",
            "error_message",
            "output_file_path",
            "output_filename",
            "total_records",
            "processing_time",
        ]

    def get_file_size_display(self, obj):
        """格式化文件大小显示"""
        size = obj.file_size
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"

    def get_output_file_size_display(self, obj):
        """格式化输出文件大小显示"""
        size = obj.output_file_size
        if not size:
            return "0 B"
        if size < 1024:
            return f"{size} B"
        elif size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"
        else:
            return f"{size / (1024 * 1024):.1f} MB"


class ProcessingLogSerializer(serializers.ModelSerializer):
    """处理日志序列化器"""

    timestamp_display = serializers.DateTimeField(
        source="timestamp", format="%Y-%m-%d %H:%M:%S", read_only=True
    )

    class Meta:
        model = ProcessingLog
        fields = ["id", "timestamp", "timestamp_display", "level", "message"]
        read_only_fields = ["id", "timestamp"]


class FileUploadSerializer(serializers.Serializer):
    """文件上传序列化器"""

    file = serializers.FileField()
    process_type = serializers.ChoiceField(
        choices=[("payment", "排单处理"), ("reimbursement", "报销处理")],
        default="payment",
    )

    def validate_file(self, value):
        """验证上传的文件"""
        # 检查文件扩展名
        if not value.name.lower().endswith((".xlsx", ".xls")):
            raise serializers.ValidationError("只支持Excel文件格式 (.xlsx, .xls)")

        # 检查文件大小 (50MB)
        if value.size > 50 * 1024 * 1024:
            raise serializers.ValidationError("文件大小不能超过50MB")

        return value
