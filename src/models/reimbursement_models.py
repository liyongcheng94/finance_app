"""
报销系统数据模型
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any
import datetime


@dataclass
class ReimbursementTopInfo:
    """报销顶部信息数据模型"""

    date: Optional[str] = None
    person: Optional[str] = None
    bank: Optional[str] = None
    bank_code: Optional[str] = None
    summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "date": self.date,
            "person": self.person,
            "bank": self.bank,
            "bankCode": self.bank_code,
            "summary": self.summary,
        }


@dataclass
class ReimbursementData:
    """报销数据模型"""

    person: Optional[str] = None
    department: Optional[str] = None
    project: Optional[str] = None
    remark: Optional[str] = None
    fee_type: Optional[str] = None
    fee_code: Optional[str] = None
    amount: Optional[float] = None
    summary: Optional[str] = None
    department_project: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "person": self.person,
            "department": self.department,
            "project": self.project,
            "remark": self.remark,
            "feeType": self.fee_type,
            "feeCode": self.fee_code,
            "amount": self.amount,
            "summary": self.summary,
            "departmentProject": self.department_project,
        }

    def is_empty(self) -> bool:
        """检查是否为空记录"""
        return all(
            value is None or value == ""
            for value in [
                self.person,
                self.department,
                self.project,
                self.remark,
                self.fee_type,
                self.fee_code,
                self.amount,
                self.summary,
            ]
        )

    def validate(self) -> tuple[bool, str]:
        """验证数据完整性"""
        if self.department_project is None or self.department_project == "":
            return False, "部门+项目不能为空"
        if self.amount is None or self.amount <= 0:
            return False, "金额必须大于0"
        if not self.person:
            return False, "报销人不能为空"
        return True, "验证通过"


@dataclass
class ReimbursementExcelRowData:
    """报销Excel行数据模型"""

    f_date: str
    f_year: str
    f_period: str
    f_group_id: str = "记"
    f_number: int = 0
    f_account_num: Optional[str] = None
    f_account_name: Optional[str] = None
    f_currency_num: str = "RMB"
    f_currency_name: str = "人民币"
    f_amount_for: Optional[float] = None
    f_debit: Optional[float] = None
    f_credit: Optional[float] = None
    f_preparer_id: str = "陈丽玲"
    f_checker_id: str = "NONE"
    f_approve_id: str = "NONE"
    f_cashier_id: str = "NONE"
    f_handler: str = ""
    f_settle_type_id: str = "*"
    f_settle_no: str = ""
    f_explanation: Optional[str] = None
    f_quantity: int = 0
    f_measure_unit_id: str = "*"
    f_unit_price: int = 0
    f_reference: str = ""
    f_trans_date: Optional[str] = None
    f_trans_no: str = ""
    f_attachments: int = 0
    f_serial_num: int = 1
    f_object_name: str = ""
    f_parameter: str = ""
    f_exchange_rate: int = 1
    f_entry_id: int = 0
    f_item: Optional[str] = None
    f_posted: int = 0
    f_internal_ind: str = ""
    f_cash_flow: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式，匹配原有的键名"""
        return {
            "FDate": self.f_date,
            "FYear": self.f_year,
            "FPeriod": self.f_period,
            "FGroupID": self.f_group_id,
            "FNumber": self.f_number,
            "FAccountNum": self.f_account_num,
            "FAccountName": self.f_account_name,
            "FCurrencyNum": self.f_currency_num,
            "FCurrencyName": self.f_currency_name,
            "FAmountFor": self.f_amount_for,
            "FDebit": self.f_debit,
            "FCredit": self.f_credit,
            "FPreparerID": self.f_preparer_id,
            "FCheckerID": self.f_checker_id,
            "FApproveID": self.f_approve_id,
            "FCashierID": self.f_cashier_id,
            "FHandler": self.f_handler,
            "FSettleTypeID": self.f_settle_type_id,
            "FSettleNo": self.f_settle_no,
            "FExplanation": self.f_explanation,
            "FQuantity": self.f_quantity,
            "FMeasureUnitID": self.f_measure_unit_id,
            "FUnitPrice": self.f_unit_price,
            "FReference": self.f_reference,
            "FTransDate": self.f_trans_date,
            "FTransNo": self.f_trans_no,
            "FAttachments": self.f_attachments,
            "FSerialNum": self.f_serial_num,
            "FObjectName": self.f_object_name,
            "FParameter": self.f_parameter,
            "FExchangeRate": self.f_exchange_rate,
            "FEntryID": self.f_entry_id,
            "FItem": self.f_item,
            "FPosted": self.f_posted,
            "FInternalInd": self.f_internal_ind,
            "FCashFlow": self.f_cash_flow,
        }
