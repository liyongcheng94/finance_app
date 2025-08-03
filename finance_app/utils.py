"""
实用工具函数
"""

import logging
from django.contrib.auth.models import User

logger = logging.getLogger("finance_app")


def get_prepared_by_display_name(user):
    """
    获取制单人的显示名称

    Args:
        user: Django User对象

    Returns:
        str: 用户显示名称，优先使用UserProfile中的display_name，
             如果没有则使用User模型的相关字段，
             最后回退到默认值
    """
    if not user:
        logger.warning("用户对象为空，使用默认制单人名称")
        return "陈丽玲"

    try:
        # 优先使用UserProfile中的display_name
        if (
            hasattr(user, "userprofile")
            and user.userprofile
            and user.userprofile.display_name
        ):
            return user.userprofile.display_name

        # 回退到User模型的字段
        if user.last_name and user.first_name:
            return f"{user.last_name}{user.first_name}"
        elif user.last_name:
            return user.last_name
        elif user.first_name:
            return user.first_name
        elif user.username:
            return user.username
        else:
            logger.warning(f"用户 {user.id} 没有可用的显示名称字段，使用默认值")
            return "陈丽玲"

    except Exception as e:
        logger.error(f"获取用户显示名称时发生错误: {str(e)}")
        return "陈丽玲"
