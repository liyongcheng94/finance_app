"""
财务应用工具函数模块
"""

from django.contrib.auth.models import User
from typing import Optional
import logging

logger = logging.getLogger("finance_app")


def get_prepared_by_display_name(user: Optional[User] = None) -> str:
    """
    获取制单人显示名称

    Args:
        user: Django用户对象，如果为None则返回默认值

    Returns:
        str: 用户显示名称，如果没有设置则返回默认值"陈丽玲"
    """
    if not user:
        logger.warning("未提供用户对象，使用默认制单人名称")
        return "陈丽玲"

    try:
        # 尝试获取用户扩展信息中的显示名称
        if hasattr(user, "profile") and user.profile:
            display_name = user.profile.display_name
            if display_name and display_name.strip():
                return display_name.strip()

        # 如果没有设置显示名称，使用用户名
        if user.username:
            logger.info(f"用户 {user.username} 未设置显示名称，使用用户名作为制单人")
            return user.username

    except Exception as e:
        logger.warning(
            f"获取用户 {user.username if user else 'Unknown'} 显示名称时出错: {str(e)}"
        )

    # 如果都获取不到，返回默认值
    logger.warning(f"无法获取用户显示名称，使用默认制单人名称")
    return "陈丽玲"


def get_prepared_by_display_name_from_user_id(user_id: Optional[int] = None) -> str:
    """
    根据用户ID获取制单人显示名称

    Args:
        user_id: 用户ID，如果为None则返回默认值

    Returns:
        str: 用户显示名称，如果没有设置则返回默认值"陈丽玲"
    """
    if not user_id:
        return "陈丽玲"

    try:
        user = User.objects.select_related("profile").get(id=user_id)
        return get_prepared_by_display_name(user)
    except User.DoesNotExist:
        logger.warning(f"用户ID {user_id} 不存在，使用默认制单人名称")
        return "陈丽玲"
    except Exception as e:
        logger.error(f"根据用户ID {user_id} 获取显示名称时出错: {str(e)}")
        return "陈丽玲"
