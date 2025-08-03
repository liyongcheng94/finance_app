"""
通用工具函数
"""

import datetime
import logging
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def setup_logging(log_filename="自动导出日志.log"):
    """设置日志配置"""
    logging.basicConfig(
        format="%(asctime)s - %(message)s",
        datefmt="%d-%b-%y %H:%M:%S",
        filename=log_filename,
        level=logging.INFO,
    )


def select_upload_file():
    """选择上传文件对话框"""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path


def exit_with_message(message):
    """显示消息并退出程序"""
    print(message)
    logging.info(message)

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Info", message)
    sys.exit(0)


def get_real_date(month_day):
    """将月日格式转换为完整日期"""
    if month_day is None:
        return None

    month_day_str = str(month_day)
    if month_day_str.find(".") == -1:
        return None

    month = month_day_str.split(".")[0]
    day = month_day_str.split(".")[1]

    # 获取当前年份
    now = datetime.datetime.now()
    year = str(now.year)
    result = year + "-" + month + "-" + day
    return datetime.datetime.strptime(result, "%Y-%m-%d")


def create_folders_if_not_exist(*folders):
    """创建文件夹如果不存在"""
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)


def get_backup_folder():
    """获取备份文件夹路径"""
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    year_folder = str(year)
    month_folder = f"{year}/{month}"
    day_folder = f"{year}/{month}/{day}"

    create_folders_if_not_exist(year_folder, month_folder, day_folder)
    return day_folder


def get_timestamp():
    """获取当前时间戳字符串"""
    return datetime.datetime.now().strftime("%H-%M-%S")
