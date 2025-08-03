"""
Excel行数据生成器
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import ACCOUNTS, DEFAULT_USERS, PAYMENT_TYPES


class ExcelRowGenerator:
    """Excel行数据生成器"""

    @staticmethod
    def generate_excel_row(row, index):
        """生成Excel行数据"""
        common_data = ExcelRowGenerator._get_common_data(row, index)

        # 获取支付类型
        payment_type = row["paymentType"]
        real_tax = row["realTax"]

        # 根据支付类型生成不同的行数据
        if payment_type == PAYMENT_TYPES["PARTIAL"]:
            result = ExcelRowGenerator._generate_partial_payment_rows(row, real_tax)
        elif payment_type == PAYMENT_TYPES["FULL"]:
            if row["realTax"] == 0:
                result = ExcelRowGenerator._generate_full_payment_exclude_tax_rows(row)
            else:
                result = ExcelRowGenerator._generate_full_payment_include_tax_rows(
                    row, real_tax
                )
        else:
            result = []

        # 合并通用数据和特定数据
        return ExcelRowGenerator._merge_rows(result, common_data)

    @staticmethod
    def _get_common_data(row, index):
        """获取通用行数据"""
        return {
            "FDate": row["FDate"],
            "FYear": row["FYear"],
            "FPeriod": row["FPeriod"],
            "FGroupID": "记",
            "FNumber": index,
            "FCurrencyNum": "RMB",
            "FCurrencyName": "人民币",
            "FPreparerID": DEFAULT_USERS["PREPARER"],
            "FCheckerID": DEFAULT_USERS["CHECKER"],
            "FApproveID": DEFAULT_USERS["APPROVE"],
            "FCashierID": DEFAULT_USERS["CASHIER"],
            "FHandler": "",
            "FSettleTypeID": "*",
            "FSettleNo": "",
            "FExplanation": row["FExplanation"],
            "FQuantity": 0,
            "FMeasureUnitID": "*",
            "FUnitPrice": 0,
            "FReference": "",
            "FTransDate": row["FDate"],
            "FTransNo": "",
            "FAttachments": 0,
            "FSerialNum": index,
            "FObjectName": "",
            "FParameter": "",
            "FExchangeRate": 1,
            "FPosted": 0,
            "FInternalInd": "",
            "FCashFlow": "",
        }

    @staticmethod
    def _generate_full_payment_include_tax_rows(row, real_tax):
        """生成全款含税行数据"""
        return [
            {
                "FAccountNum": row["feeCode"],
                "FAccountName": row["feeType"],
                "FAmountFor": row["remain"],
                "FDebit": row["remain"],
                "FCredit": 0,
                "FEntryID": 0,
                "FItem": row["depProjectStr"],
            },
            {
                "FAccountNum": ACCOUNTS["TAX"],
                "FAccountName": "进项税额",
                "FAmountFor": real_tax,
                "FDebit": real_tax,
                "FCredit": 0,
                "FEntryID": 1,
                "FItem": "",
            },
            {
                "FAccountNum": ACCOUNTS["SUPPLIER"],
                "FAccountName": "应付供应商",
                "FAmountFor": row["totalAmount"],
                "FDebit": 0,
                "FCredit": row["totalAmount"],
                "FEntryID": 2,
                "FItem": row["supplierProjectStr"],
            },
            {
                "FAccountNum": ACCOUNTS["SUPPLIER"],
                "FAccountName": "应付供应商",
                "FAmountFor": row["totalAmount"],
                "FDebit": row["totalAmount"],
                "FCredit": 0,
                "FEntryID": 3,
                "FItem": row["supplierProjectStr"],
            },
            {
                "FAccountNum": row["FAccountNum_Bank"],
                "FAccountName": "银行",
                "FAmountFor": row["totalAmount"],
                "FDebit": 0,
                "FCredit": row["totalAmount"],
                "FEntryID": 4,
                "FItem": "",
            },
        ]

    @staticmethod
    def _generate_full_payment_exclude_tax_rows(row):
        """生成全款不含税行数据"""
        return [
            {
                "FAccountNum": row["feeCode"],
                "FAccountName": row["feeType"],
                "FAmountFor": row["remain"],
                "FDebit": row["remain"],
                "FCredit": 0,
                "FEntryID": 0,
                "FItem": row["depProjectStr"],
            },
            {
                "FAccountNum": ACCOUNTS["SUPPLIER"],
                "FAccountName": "应付供应商",
                "FAmountFor": row["totalAmount"],
                "FDebit": 0,
                "FCredit": row["totalAmount"],
                "FEntryID": 1,
                "FItem": row["supplierProjectStr"],
            },
            {
                "FAccountNum": ACCOUNTS["SUPPLIER"],
                "FAccountName": "应付供应商",
                "FAmountFor": row["totalAmount"],
                "FDebit": row["totalAmount"],
                "FCredit": 0,
                "FEntryID": 2,
                "FItem": row["supplierProjectStr"],
            },
            {
                "FAccountNum": row["FAccountNum_Bank"],
                "FAccountName": "银行",
                "FAmountFor": row["totalAmount"],
                "FDebit": 0,
                "FCredit": row["totalAmount"],
                "FEntryID": 3,
                "FItem": "",
            },
        ]

    @staticmethod
    def _generate_partial_payment_include_tax_rows(row, real_tax):
        """生成定金含税行数据"""
        return [
            {
                "FAccountNum": row["feeCode"],
                "FAccountName": row["feeType"],
                "FAmountFor": real_tax,
                "FDebit": real_tax,
                "FCredit": 0,
                "FEntryID": 0,
                "FItem": row["depProjectStr"],
            },
            {
                "FAccountNum": ACCOUNTS["TRANSIT"],
                "FAccountName": "在途物资",
                "FAmountFor": row["remain"],
                "FDebit": row["remain"],
                "FCredit": 0,
                "FEntryID": 1,
                "FItem": "",
            },
            {
                "FAccountNum": ACCOUNTS["SUPPLIER"],
                "FAccountName": "应付供应商",
                "FAmountFor": row["totalAmount"],
                "FDebit": 0,
                "FCredit": row["totalAmount"],
                "FEntryID": 2,
                "FItem": row["supplierProjectStr"],
            },
            {
                "FAccountNum": ACCOUNTS["SUPPLIER"],
                "FAccountName": "应付供应商",
                "FAmountFor": real_tax,
                "FDebit": real_tax,
                "FCredit": 0,
                "FEntryID": 3,
                "FItem": row["supplierProjectStr"],
            },
            {
                "FAccountNum": row["FAccountNum_Bank"],
                "FAccountName": "银行",
                "FAmountFor": real_tax,
                "FDebit": 0,
                "FCredit": real_tax,
                "FEntryID": 4,
                "FItem": "",
            },
        ]

    @staticmethod
    def _merge_rows(unique_list, common_data):
        """合并行数据"""
        result = []
        for row in unique_list:
            result.append({**row, **common_data})
        return result

    @staticmethod
    def generate_excel_data(data):
        """生成所有Excel数据"""
        excel_data = []
        index = 0

        for row in data:
            index = index + 1
            excel_data.append(ExcelRowGenerator.generate_excel_row(row, index))

        return excel_data
