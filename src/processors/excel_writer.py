"""
统一Excel文件写入功能 - 支持排单和报销双模式
"""

import json
import sys
import xlsxwriter
import os
from typing import List, Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tkinter import messagebox
from unified_config import PaymentConfig, ReimbursementConfig


class UnifiedExcelWriter:
    """统一Excel文件写入器"""

    def __init__(self, file_path: str, file_type: str = "payment"):
        self.file_path = file_path
        self.file_type = file_type
        self.workbook = None

        # 根据文件类型选择配置
        if file_type == "reimbursement":
            self.config = ReimbursementConfig()
        else:
            self.config = PaymentConfig()

    def write_excel(self, data: List[Dict[str, Any]]) -> bool:
        """写入Excel文件"""
        try:
            self.workbook = xlsxwriter.Workbook(self.file_path)

            # 写入schema工作表
            self._write_schema_sheet()

            # 写入数据工作表
            self._write_data_sheet(data)

            # 保存文件
            self.workbook.close()
            return True

        except Exception as e:
            # 提示用户关闭文件
            messagebox.showerror(
                "文件正在被占用", "请先关闭自动导出的相关文件再进行操作！"
            )
            return False

    def _write_schema_sheet(self):
        """写入schema工作表"""
        worksheet = self.workbook.add_worksheet("t_Schema")

        # 读取JSON schema数据
        try:
            with open(self.config.SCHEMA_FILENAME, "r", encoding="utf-8") as f:
                schema = json.load(f)
        except FileNotFoundError:
            schema = []

        # 写入表头
        for i, header in enumerate(self.config.SCHEMA_HEADERS):
            worksheet.write(0, i, header)

        # 写入schema数据
        for i, schema_item in enumerate(schema):
            for j, header in enumerate(self.config.SCHEMA_HEADERS):
                value = schema_item.get(header, "")
                worksheet.write(i + 1, j, value)

    def _write_data_sheet(self, data: List[Dict[str, Any]]):
        """写入数据工作表"""
        worksheet = self.workbook.add_worksheet("Page1")

        # 写入表头
        for i, header in enumerate(self.config.EXCEL_HEADERS):
            worksheet.write(0, i, header)

        # 写入数据
        if self.file_type == "reimbursement":
            self._write_reimbursement_data(worksheet, data)
        else:
            self._write_payment_data(worksheet, data)

    def _write_reimbursement_data(self, worksheet, data: List[Dict[str, Any]]):
        """写入报销数据"""
        for i, row_data in enumerate(data):
            for j, header in enumerate(self.config.EXCEL_HEADERS):
                if j == 9 and header == "FAmountFor":  # FAmountFor列使用公式
                    worksheet.write(i + 1, j, f"=SUM(K{i + 2}+L{i + 2})")
                else:
                    worksheet.write(i + 1, j, row_data.get(header, ""))

    def _write_payment_data(self, worksheet, data: List[Dict[str, Any]]):
        """写入排单数据"""
        sum_row = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                sum_row = sum_row + 1
                for k, header in enumerate(self.config.EXCEL_HEADERS):
                    if header in data[i][j]:
                        worksheet.write(sum_row, k, data[i][j][header])

    def create_output_file_path(self, output_folder: str, filename: str) -> str:
        """创建输出文件路径"""
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        return os.path.join(output_folder, filename)


# 为了向后兼容，保留原来的ExcelWriter类
class ExcelWriter(UnifiedExcelWriter):
    """Excel文件写入器 - 向后兼容"""

    def __init__(self, file_path):
        super().__init__(file_path, "payment")
