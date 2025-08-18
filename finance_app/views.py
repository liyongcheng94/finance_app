import os
import time
from django.shortcuts import render
from django.http import FileResponse, Http404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .models import FinanceRecord, ProcessingLog
from .serializers import (
    FinanceRecordSerializer,
    ProcessingLogSerializer,
    FileUploadSerializer,
)
from .services.excel_processor import ExcelProcessor, ExcelProcessingError
import logging


class FinanceRecordViewSet(viewsets.ModelViewSet):
    """财务记录视图集"""

    queryset = FinanceRecord.objects.all()
    serializer_class = FinanceRecordSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """获取查询集，只返回当前用户的记录"""
        queryset = FinanceRecord.objects.filter(user=self.request.user)

        # 状态过滤
        status_filter = self.request.query_params.get("status", None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 处理类型过滤
        process_type_filter = self.request.query_params.get("process_type", None)
        if process_type_filter:
            queryset = queryset.filter(process_type=process_type_filter)

        # 日期过滤
        date_from = self.request.query_params.get("date_from", None)
        if date_from:
            queryset = queryset.filter(upload_time__date__gte=date_from)

        date_to = self.request.query_params.get("date_to", None)
        if date_to:
            queryset = queryset.filter(upload_time__date__lte=date_to)

        # 按上传时间倒序排列
        return queryset.order_by("-upload_time")

    @action(
        detail=False, methods=["post"], parser_classes=[MultiPartParser, FormParser]
    )
    def upload(self, request):
        """
        上传Excel文件并处理
        """
        serializer = FileUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        uploaded_file = serializer.validated_data["file"]
        process_type = serializer.validated_data["process_type"]

        # 创建财务记录
        finance_record = FinanceRecord.objects.create(
            user=request.user,
            filename=uploaded_file.name,
            file_path=uploaded_file,
            process_type=process_type,
            status="pending",
        )

        # 添加初始日志
        ProcessingLog.objects.create(
            record=finance_record,
            level="INFO",
            message=f"文件上传成功: {uploaded_file.name}",
        )

        try:
            # 处理Excel文件
            start_time = time.time()
            processor = ExcelProcessor()

            # 添加处理开始日志
            process_type_display = "排单" if process_type == "payment" else "报销"
            ProcessingLog.objects.create(
                record=finance_record,
                level="INFO",
                message=f"开始处理{process_type_display}Excel文件...",
            )

            output_path, record_count = processor.process_excel_file(
                finance_record.file_path.path, process_type
            )
            processing_time = time.time() - start_time

            # 更新记录状态
            finance_record.status = "completed"
            finance_record.output_file_path.name = os.path.relpath(
                output_path, settings.MEDIA_ROOT
            )
            finance_record.output_filename = os.path.basename(output_path)
            finance_record.total_records = record_count
            finance_record.processing_time = processing_time
            finance_record.save()

            # 添加成功日志
            ProcessingLog.objects.create(
                record=finance_record,
                level="INFO",
                message=f"Excel文件处理完成，共处理 {record_count} 条记录，耗时 {processing_time:.2f} 秒",
            )

            # 返回处理结果
            return Response(
                {
                    "id": finance_record.id,
                    "status": "completed",
                    "message": f"文件处理成功，共处理 {record_count} 条记录",
                    "output_filename": finance_record.output_filename,
                    "processing_time": processing_time,
                    "total_records": record_count,
                },
                status=status.HTTP_201_CREATED,
            )

        except ExcelProcessingError as e:
            # 处理业务逻辑错误
            finance_record.status = "failed"
            finance_record.error_message = str(e)
            finance_record.save()

            ProcessingLog.objects.create(
                record=finance_record, level="ERROR", message=f"Excel处理失败: {str(e)}"
            )

            return Response(
                {"id": finance_record.id, "status": "failed", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # 处理系统错误
            finance_record.status = "failed"
            finance_record.error_message = f"系统错误: {str(e)}"
            finance_record.save()

            ProcessingLog.objects.create(
                record=finance_record, level="ERROR", message=f"系统错误: {str(e)}"
            )

            logger = logging.getLogger("finance_app")
            logger.error(f"处理Excel文件时发生系统错误: {str(e)}", exc_info=True)

            return Response(
                {
                    "id": finance_record.id,
                    "status": "failed",
                    "error": "系统内部错误，请联系管理员",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        """
        下载处理后的Excel文件
        """
        try:
            finance_record = self.get_object()

            if (
                finance_record.status != "completed"
                or not finance_record.output_file_path
            ):
                return Response(
                    {"error": "文件尚未处理完成或处理失败"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            file_path = finance_record.output_file_path.path
            if not os.path.exists(file_path):
                return Response(
                    {"error": "文件不存在"}, status=status.HTTP_404_NOT_FOUND
                )

            # 记录下载日志
            ProcessingLog.objects.create(
                record=finance_record,
                level="INFO",
                message=f"文件下载: {finance_record.output_filename}",
            )

            response = FileResponse(
                open(file_path, "rb"),
                as_attachment=True,
                filename=finance_record.output_filename,
            )
            return response

        except Exception as e:
            return Response(
                {"error": f"下载文件时发生错误: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=True, methods=["get"])
    def logs(self, request, pk=None):
        """
        获取处理日志
        """
        finance_record = self.get_object()
        logs = ProcessingLog.objects.filter(record=finance_record).order_by(
            "-timestamp"
        )
        serializer = ProcessingLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def history(self, request):
        """
        获取处理历史记录
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@login_required(login_url="/auth/login/")
def index(request):
    """首页视图"""
    return render(request, "index.html")


@login_required(login_url="/auth/login/")
def history(request):
    """历史记录页面"""
    return render(request, "history.html")
