"""
配置文件和常量定义
"""

import os

# 日志配置
LOG_FORMAT = "%(asctime)s - %(message)s"
LOG_DATE_FORMAT = "%d-%b-%y %H:%M:%S"
LOG_FILENAME = "自动导出日志.log"

# Excel相关配置
DEFAULT_SHEET_NAME = "付款(每日)"
SCHEMA_FILENAME = "t_Schema.json"

# 文件夹配置
OUTPUT_FOLDER = "最新"
BACKUP_FOLDER_PATTERN = "{year}/{month}/{day}"

# 银行账户映射
BANK_ACCOUNT_MAPPING = {
    "东蜜代深蜜支付：": "1002.16",
    "深蜜代东蜜付：": "1002.21",
    "深蜜支付：": "1002.21",
    "高定支付：": "1002.30.01",
    "高定付：": "1002.30.02",
}

# 默认银行账户
DEFAULT_BANK_ACCOUNT = "1002.16"

# 键映射配置
KEY_MAPPINGS = {
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
    },
    "supplier": {
        "简称": "shortName",
        "代码": "code",
        "名称": "name",
        "全名": "fullName",
    },
    "project": {
        "项目简称": "shortName",
        "代码": "code",
        "名称": "name",
        "全名": "fullName",
    },
    "feeType": {"别称": "alias", "科目名称": "name", "科目代码": "code"},
}

# Excel输出表头
EXCEL_HEADERS = [
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
]

# Schema表头
SCHEMA_HEADERS = [
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
]

# 支付类型
PAYMENT_TYPES = {"PARTIAL": "partial", "FULL": "full"}

# 账户配置
ACCOUNTS = {"TAX": "2221.01.01", "SUPPLIER": "2202.01", "TRANSIT": "1402"}

# 部门配置
DEPARTMENT_CONFIG = {"CODE": "02", "NAME": "采购部", "STRING": "部门---02---采购部"}

# 默认用户配置
DEFAULT_USERS = {
    "PREPARER": "陈丽玲",  # 默认制单人，实际使用时会被动态用户名替换
    "CHECKER": "NONE",
    "APPROVE": "NONE",
    "CASHIER": "NONE",
}
