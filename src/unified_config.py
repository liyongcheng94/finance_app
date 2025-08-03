"""
统一配置文件 - 支持排单和报销两种模式
"""

import os

# 日志配置
LOG_FORMAT = "%(asctime)s - %(message)s"
LOG_DATE_FORMAT = "%d-%b-%y %H:%M:%S"
LOG_FILENAME = "自动导出日志.log"

# 通用配置
OUTPUT_FOLDER = "最新"
SCHEMA_FILENAME = "t_Schema.json"


# 文件类型枚举
class FileType:
    PAYMENT = "payment"  # 排单
    REIMBURSEMENT = "reimbursement"  # 报销


# 排单配置
PAYMENT_CONFIG = {
    "DEFAULT_SHEET_NAME": "付款(每日)",
    "BANK_ACCOUNT_MAPPING": {
        "东蜜代深蜜支付：": "1002.16",
        "深蜜代东蜜付：": "1002.21",
        "深蜜支付：": "1002.21",
        "高定支付：": "1002.30.01",
        "高定付：": "1002.30.02",
    },
    "DEFAULT_BANK_ACCOUNT": "1002.16",
    "KEY_MAPPINGS": {
        "pay": {
            "日期": "date",
            "支付公司": "company",
            "项目简称（保持一致）": "project",
            "户型": "houseType",
            "供应商": "supplier",
            "费用类型": "feeType",
            "付款方式": "paymentType",
            "总金额": "totalAmount",
            "税": "tax",
            "备注1": "remark1",
            "备注2": "remark2",
            "摘要": "FExplanation",
        }
    },
}

# 报销配置
REIMBURSEMENT_CONFIG = {
    "DEFAULT_SHEET_NAME": "报销  (每日)",
    "EXCEL_HEADERS": [
        "FDate",
        "FYear",
        "FPeriod",
        "FGroupID",
        "FNumber",
        "FAccountNum",
        "FAccountName",
        "FCurrencyNum",
        "FCurrencyName",
        "FAmountFor",
        "FDebit",
        "FCredit",
        "FPreparerID",
        "FCheckerID",
        "FApproveID",
        "FCashierID",
        "FHandler",
        "FSettleTypeID",
        "FSettleNo",
        "FExplanation",
        "FQuantity",
        "FMeasureUnitID",
        "FUnitPrice",
        "FReference",
        "FTransDate",
        "FTransNo",
        "FAttachments",
        "FSerialNum",
        "FObjectName",
        "FParameter",
        "FExchangeRate",
        "FEntryID",
        "FItem",
        "FPosted",
        "FInternalInd",
        "FCashFlow",
    ],
    "SCHEMA_HEADERS": [
        "FType",
        "FKey",
        "FFieldName",
        "FCaption",
        "FValueType",
        "FNeedSave",
        "FColIndex",
        "FSrcTableName",
        "FSrcFieldName",
        "FExpFieldName",
        "FImpFieldName",
        "FDefaultVal",
        "FSearch",
        "FItemPageName",
        "FTrueType",
        "FPrecision",
        "FSearchName",
        "FIsShownList",
        "FViewMask",
        "FPage",
    ],
    "REIMBURSEMENT_COLUMNS": {
        "person": 0,  # 报销人
        "department": 1,  # 部门代码
        "project": 2,  # 项目简称（保持一致）
        "remark": 3,  # 备注
        "fee": 4,  # 费用别称
        "feeType": 5,  # 费用类型
        "feeCode": 6,  # 费用代码
        "amount": 7,  # 金额
        "summary": 8,  # 摘要
        "departmentProject": 9,  # 部门+项目
    },
    "TOP_INFO_COLUMNS": {
        "date": 1,  # 日期
        "person": 3,  # 报销人
        "bank": 5,  # 银行
        "bankCode": 7,  # 银行代码
        "summary": 9,  # 摘要
    },
    "DEFAULT_VALUES": {
        "FCurrencyNum": "RMB",
        "FCurrencyName": "人民币",
        "FPreparerID": "陈丽玲",  # 默认制单人，实际使用时会被动态用户名替换
        "FCheckerID": "NONE",
        "FApproveID": "NONE",
        "FCashierID": "NONE",
        "FHandler": "",
        "FSettleTypeID": "*",
        "FSettleNo": "",
        "FQuantity": 0,
        "FMeasureUnitID": "*",
        "FUnitPrice": 0,
        "FReference": "",
        "FTransNo": "",
        "FAttachments": 0,
        "FSerialNum": 1,
        "FObjectName": "",
        "FParameter": "",
        "FExchangeRate": 1,
        "FPosted": 0,
        "FInternalInd": "",
        "FCashFlow": "",
        "FGroupID": "记",
    },
}
