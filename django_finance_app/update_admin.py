#!/usr/bin/env python
"""
更新管理员用户信息的脚本
用法: python update_admin.py
"""

import os
import sys
import django

# 添加项目路径到系统路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_project.settings")

# 初始化Django
django.setup()

from django.contrib.auth.models import User


def update_admin_user():
    """更新管理员用户信息"""
    try:
        # 尝试获取ID为1的用户
        admin_user = User.objects.get(id=1)
        print(f"找到现有管理员用户: {admin_user.username}")

        # 更新用户信息
        old_username = admin_user.username
        admin_user.username = "will.li"
        admin_user.email = "will.li@example.com"
        admin_user.set_password("kumshing")

        # 确保管理员权限
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.is_active = True

        # 保存更改
        admin_user.save()

        print("=" * 50)
        print("管理员用户更新成功!")
        print("=" * 50)
        print(f"原用户名: {old_username}")
        print(f"新用户名: {admin_user.username}")
        print(f"新邮箱: {admin_user.email}")
        print(f"新密码: kumshing")
        print(f"用户ID: {admin_user.id}")
        print(f"超级用户: {admin_user.is_superuser}")
        print(f"员工权限: {admin_user.is_staff}")
        print(f"账户激活: {admin_user.is_active}")
        print("=" * 50)

    except User.DoesNotExist:
        print("ID为1的用户不存在，创建新的管理员用户...")

        # 创建新的超级用户
        admin_user = User.objects.create_superuser(
            username="will.li", email="will.li@example.com", password="kumshing"
        )

        print("=" * 50)
        print("新管理员用户创建成功!")
        print("=" * 50)
        print(f"用户名: {admin_user.username}")
        print(f"邮箱: {admin_user.email}")
        print(f"密码: kumshing")
        print(f"用户ID: {admin_user.id}")
        print(f"超级用户: {admin_user.is_superuser}")
        print(f"员工权限: {admin_user.is_staff}")
        print(f"账户激活: {admin_user.is_active}")
        print("=" * 50)

    except Exception as e:
        print(f"更新管理员用户时出错: {str(e)}")
        return False

    return True


def verify_admin_login():
    """验证管理员登录"""
    from django.contrib.auth import authenticate

    print("\n验证新的管理员登录信息...")
    user = authenticate(username="will.li", password="kumshing")

    if user is not None and user.is_superuser:
        print("✅ 管理员登录验证成功!")
        print(f"✅ 用户名: {user.username}")
        print(f"✅ 超级用户权限: {user.is_superuser}")
    else:
        print("❌ 管理员登录验证失败!")
        return False

    return True


def main():
    """主函数"""
    print("开始更新管理员用户信息...")
    print("目标用户名: will.li")
    print("目标密码: kumshing")
    print("-" * 50)

    # 更新管理员用户
    if update_admin_user():
        # 验证登录
        if verify_admin_login():
            print("\n🎉 管理员用户更新完成且验证成功!")
            print("\n现在可以使用以下信息登录:")
            print("用户名: will.li")
            print("密码: kumshing")
        else:
            print("\n⚠️ 管理员用户更新完成但验证失败，请检查配置!")
    else:
        print("\n❌ 管理员用户更新失败!")


if __name__ == "__main__":
    main()
