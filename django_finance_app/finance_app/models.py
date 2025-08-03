from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os


class UserProfile(models.Model):
    """用户扩展信息模型"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile", verbose_name="用户账号"
    )
    display_name = models.CharField(
        max_length=50, verbose_name="用户名", help_text="用于显示的用户名称，如：陈丽玲"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "user_profiles"
        verbose_name = "用户扩展信息"
        verbose_name_plural = "用户扩展信息"

    def __str__(self):
        return f"{self.user.username} - {self.display_name}"


class FinanceRecord(models.Model):
    """财务记录模型"""

    STATUS_CHOICES = [
        ("pending", "处理中"),
        ("completed", "已完成"),
        ("failed", "失败"),
    ]

    PROCESS_TYPE_CHOICES = [
        ("payment", "排单处理"),
        ("reimbursement", "报销处理"),
    ]

    # 基本信息
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="finance_records",
        verbose_name="用户",
    )
    upload_time = models.DateTimeField(default=timezone.now, verbose_name="上传时间")
    filename = models.CharField(max_length=255, verbose_name="原始文件名")
    file_path = models.FileField(upload_to="uploads/", verbose_name="上传文件路径")
    process_type = models.CharField(
        max_length=20,
        choices=PROCESS_TYPE_CHOICES,
        default="payment",
        verbose_name="处理类型",
    )

    # 处理状态
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="处理状态",
    )
    error_message = models.TextField(blank=True, null=True, verbose_name="错误信息")

    # 结果文件
    output_file_path = models.FileField(
        upload_to="outputs/", blank=True, null=True, verbose_name="输出文件路径"
    )
    output_filename = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="输出文件名"
    )

    # 统计信息
    total_records = models.IntegerField(default=0, verbose_name="处理记录数")
    processing_time = models.FloatField(default=0.0, verbose_name="处理时间(秒)")

    class Meta:
        db_table = "finance_records"
        verbose_name = "财务记录"
        verbose_name_plural = "财务记录"
        ordering = ["-upload_time"]

    def __str__(self):
        return f"{self.filename} - {self.get_status_display()}"

    @property
    def file_size(self):
        """获取文件大小"""
        if self.file_path and os.path.exists(self.file_path.path):
            return os.path.getsize(self.file_path.path)
        return 0

    @property
    def output_file_size(self):
        """获取输出文件大小"""
        if self.output_file_path and os.path.exists(self.output_file_path.path):
            return os.path.getsize(self.output_file_path.path)
        return 0


class ProcessingLog(models.Model):
    """处理日志模型"""

    record = models.ForeignKey(
        FinanceRecord,
        on_delete=models.CASCADE,
        related_name="logs",
        verbose_name="财务记录",
    )
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="时间戳")
    level = models.CharField(max_length=10, default="INFO", verbose_name="日志级别")
    message = models.TextField(verbose_name="日志信息")

    class Meta:
        db_table = "processing_logs"
        verbose_name = "处理日志"
        verbose_name_plural = "处理日志"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.record.filename} - {self.level} - {self.timestamp}"
