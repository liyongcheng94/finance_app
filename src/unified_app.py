"""
统一的财务处理应用 - 支持排单和报销
"""

import logging
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox

# 添加路径以便导入其他模块
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from file_type_detector import FileTypeDetector
from unified_config import FileType, PaymentConfig, ReimbursementConfig
from processors.reimbursement_processor import ReimbursementProcessor
from processors.excel_writer import UnifiedExcelWriter


class UnifiedFinanceApp:
    """统一的财务处理应用"""

    def __init__(self):
        self.file_type = None
        self.file_path = None
        self.detector = FileTypeDetector()

    def select_file(self) -> str:
        """选择输入文件"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
        )

        if not file_path:
            self.exit_with_message("未选择文件")

        return file_path

    def detect_file_type(self, file_path: str) -> str:
        """检测文件类型"""
        try:
            file_type = self.detector.detect_file_type(file_path)
            return file_type
        except Exception as e:
            # 如果自动检测失败，询问用户
            return self.ask_user_file_type()

    def ask_user_file_type(self) -> str:
        """询问用户文件类型"""
        root = tk.Tk()
        root.withdraw()

        result = messagebox.askyesnocancel(
            "文件类型选择",
            "无法自动识别文件类型，请选择：\n\n是(Yes) = 报销文件\n否(No) = 排单文件\n取消(Cancel) = 退出",
        )

        if result is None:  # Cancel
            self.exit_with_message("用户取消操作")
        elif result:  # Yes
            return "reimbursement"
        else:  # No
            return "payment"

    def process_reimbursement(self, file_path: str):
        """处理报销文件"""
        try:
            # 使用报销处理器
            processor = ReimbursementProcessor()
            result_data = processor.process_file(file_path)

            if not result_data:
                self.exit_with_message("报销文件处理失败，未获得有效数据")

            # 生成输出文件路径
            from pathlib import Path

            input_name = Path(file_path).stem
            output_name = f"{input_name}-自动导出.xlsx"
            output_dir = os.path.join(os.path.dirname(file_path), "最新")

            # 创建Excel写入器并写入结果
            writer = UnifiedExcelWriter("", "reimbursement")
            output_path = writer.create_output_file_path(output_dir, output_name)
            writer.file_path = output_path

            if writer.write_excel(result_data):
                self.exit_with_message(f"报销文件处理完成！\n输出文件: {output_path}")
            else:
                self.exit_with_message("Excel文件写入失败")

        except Exception as e:
            self.exit_with_message(f"报销文件处理失败：{str(e)}")

    def process_payment(self, file_path: str):
        """处理排单文件"""
        try:
            # 使用原有的排单处理逻辑
            # 这里需要调用原有的排单处理代码
            messagebox.showinfo(
                "提示",
                "排单文件处理功能正在集成中...\n请使用原有的main.py文件处理排单文件",
            )
            # TODO: 集成原有的排单处理逻辑

        except Exception as e:
            self.exit_with_message(f"排单文件处理失败：{str(e)}")

    def exit_with_message(self, message: str):
        """显示消息并退出"""
        print(message)
        messagebox.showinfo("提示", message)
        sys.exit(0)

    def run(self):
        """运行主程序"""
        try:
            print("=" * 60)
            print("统一财务处理系统启动")
            print("支持：排单Excel处理 | 报销Excel处理")
            print("=" * 60)

            # 1. 选择文件
            self.file_path = self.select_file()
            print(f"选择的文件: {self.file_path}")

            # 2. 检测文件类型
            self.file_type = self.detect_file_type(self.file_path)
            file_type_name = (
                "报销文件" if self.file_type == "reimbursement" else "排单文件"
            )
            print(f"检测到文件类型: {file_type_name}")

            messagebox.showinfo("文件类型", f"检测到文件类型：{file_type_name}")

            # 3. 根据文件类型处理
            if self.file_type == "reimbursement":
                self.process_reimbursement(self.file_path)
            elif self.file_type == "payment":
                self.process_payment(self.file_path)
            else:
                self.exit_with_message("未知的文件类型")

        except Exception as e:
            self.exit_with_message(f"程序执行出错：{str(e)}")


def main():
    """主函数"""
    # 设置日志
    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        filename="自动导出日志.log",
        level=logging.INFO,
    )

    # 创建并运行应用
    app = UnifiedFinanceApp()
    app.run()


if __name__ == "__main__":
    main()
