"""
数据处理和转换功能
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import BANK_ACCOUNT_MAPPING, DEFAULT_BANK_ACCOUNT, PAYMENT_TYPES
from utils.helpers import exit_with_message, get_real_date


class DataProcessor:
    """数据处理器"""

    @staticmethod
    def get_real_tax(row):
        """计算实际税额"""
        payment_type = row["paymentType"]
        remark2 = row["remark2"]
        tax = row["tax"]
        real_tax = 0

        if payment_type == PAYMENT_TYPES["PARTIAL"]:
            # 备注2示例: （1050+2450）
            real_tax = DataProcessor.get_fee_by_remark2(remark2)
        else:
            real_tax = tax

        # 如果real_tax为None或空字符串
        if not real_tax:
            real_tax = 0

        return float(real_tax)

    @staticmethod
    def get_fee_code(fee_type_data, fee_type):
        """获取费用代码"""
        for item in fee_type_data:
            if item["name"] == fee_type:
                return str(item["code"])
            if fee_type == item["name"] + "费":
                return str(item["code"])
            if fee_type == item["alias"]:
                return str(item["code"])
            if fee_type == item["alias"] + "费":
                return str(item["code"])
        return None

    @staticmethod
    def get_fee_by_remark2(remark2):
        """从备注2中提取费用"""
        if not remark2:
            exit_with_message("请检查有定价的项目 备注2是否填写")

        fee = 0
        # 备注2示例: （1050+2450）
        if "（" in remark2 and "）" in remark2:
            remark2 = remark2.replace("（", "").replace("）", "")
            fee = remark2.split("+")
            fee = fee[0]
        return fee

    @staticmethod
    def append_data(base_data, supplier_data, project_data, fee_type_data):
        """合并和处理数据"""
        cannot_find = []

        for i in range(len(base_data)):
            row = base_data[i]
            row["supplierStr"] = ""
            row["projectStr"] = ""

            # 查找供应商信息
            for supplier in supplier_data:
                if supplier["shortName"] == row["supplier"]:
                    row["supplierStr"] = (
                        "供应商---" + str(supplier["code"]) + "---" + supplier["name"]
                    )
                    break

            # 查找项目信息
            for project in project_data:
                if project["shortName"] == row["project"]:
                    row["projectStr"] = (
                        "项目---" + str(project["code"]) + "---" + project["name"]
                    )
                    break

            # 检查是否找到匹配项
            if not row["supplierStr"]:
                error_string = "找不到供应商: " + row["supplier"]
                cannot_find.append(i)

            if not row["projectStr"]:
                cannot_find.append(row["project"])

            # 如果有找不到的项目，跳过处理
            if len(cannot_find) > 0:
                print(cannot_find)
                continue

            # 设置部门和项目字符串
            row["depStr"] = "部门---02---采购部"
            row["depProjectStr"] = row["depStr"] + "," + row["projectStr"]
            row["supplierProjectStr"] = row["supplierStr"] + "," + row["projectStr"]

            # 设置银行账户
            pay_company = row["company"]
            row["FAccountNum_Bank"] = BANK_ACCOUNT_MAPPING.get(
                pay_company, DEFAULT_BANK_ACCOUNT
            )

            # 获取费用代码
            row["feeCode"] = DataProcessor.get_fee_code(fee_type_data, row["feeType"])

            # 处理日期
            real_date = get_real_date(row["date"])
            row["FDate"] = real_date.strftime("%Y-%m-%d")
            row["FYear"] = real_date.strftime("%Y")
            row["FPeriod"] = real_date.strftime("%m")

            # 处理支付类型
            payment_type = row["paymentType"]
            if "定金" in payment_type:
                row["paymentType"] = PAYMENT_TYPES["PARTIAL"]
            if "全款" in payment_type:
                row["paymentType"] = PAYMENT_TYPES["FULL"]

            # 计算税额和剩余金额
            real_tax = DataProcessor.get_real_tax(row)
            row["realTax"] = real_tax
            row["remain"] = row["totalAmount"] - real_tax

        if len(cannot_find) > 0:
            print(cannot_find)
            exit_with_message("请检查项目或供应商：" + str(cannot_find) + "是否正确")

        return base_data
