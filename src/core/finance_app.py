"""
主应用逻辑
"""

import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import KEY_MAPPINGS, DEFAULT_SHEET_NAME, OUTPUT_FOLDER
from processors.excel_parser import ExcelParser
from processors.data_processor import DataProcessor
from processors.excel_generator import ExcelRowGenerator
from processors.excel_writer import ExcelWriter
from utils.helpers import (
    select_upload_file,
    exit_with_message,
    create_folders_if_not_exist,
    get_backup_folder,
    get_timestamp,
)


class FinanceApp:
    """财务处理应用"""

    def __init__(self):
        self.file_path = None
        self.parser = None

    def run(self):
        """运行应用主逻辑"""
        try:
            # 选择文件
            self.file_path = select_upload_file()
            if not self.file_path:
                exit_with_message("未选择文件")

            # 初始化解析器
            self.parser = ExcelParser(self.file_path)

            # 解析基础数据
            base_data = self._parse_base_data()

            # 解析辅助数据
            supplier_data, project_data, fee_type_data = self._parse_auxiliary_data(
                base_data
            )

            # 处理数据
            processed_data = DataProcessor.append_data(
                base_data, supplier_data, project_data, fee_type_data
            )

            # 生成Excel数据
            excel_data = ExcelRowGenerator.generate_excel_data(processed_data)

            # 写入文件
            output_path = self._write_output_file(excel_data)

            # 备份文件
            self._backup_file(output_path)

            # 完成
            exit_with_message(f"导出成功！文件路径： {os.path.abspath(output_path)}")

        except Exception as e:
            exit_with_message(f"处理失败: {str(e)}")
        finally:
            if self.parser:
                self.parser.close()

    def _parse_base_data(self):
        """解析基础数据"""
        return self.parser.parse_sheet(
            DEFAULT_SHEET_NAME,
            key_map=KEY_MAPPINGS["pay"],
            max_col=12,
            start_row=3,
            header_row=2,
        )

    def _parse_auxiliary_data(self, base_data):
        """解析辅助数据"""
        # 提取供应商列表
        supplier_check_list = [item["supplier"] for item in base_data]

        # 解析费用类型数据
        fee_type_data = self.parser.parse_sheet(
            "核算项目_费用代码", max_col=3, key_map=KEY_MAPPINGS["feeType"]
        )

        # 解析项目数据
        project_data = self.parser.parse_sheet(
            "核算项目_项目", key_map=KEY_MAPPINGS["project"]
        )

        # 解析供应商数据
        supplier_data = self.parser.parse_supplier_helper(
            "核算项目_供应商",
            key_map=KEY_MAPPINGS["supplier"],
            check_list=supplier_check_list,
        )

        return supplier_data, project_data, fee_type_data

    def _write_output_file(self, excel_data):
        """写入输出文件"""
        # 创建输出文件夹
        create_folders_if_not_exist(OUTPUT_FOLDER)

        # 生成文件名
        file_name = "排单-最新.xlsx"
        output_path = os.path.join(OUTPUT_FOLDER, file_name)

        # 写入Excel文件
        writer = ExcelWriter(output_path)
        writer.write_excel(excel_data)

        return output_path

    def _backup_file(self, output_path):
        """备份文件"""
        # 获取备份文件夹
        backup_folder = get_backup_folder()

        # 生成备份文件名
        timestamp = get_timestamp()
        backup_file_name = f"排单-{timestamp}.xlsx"
        backup_path = os.path.join(backup_folder, backup_file_name)

        # 复制文件
        shutil.copy(output_path, backup_path)
