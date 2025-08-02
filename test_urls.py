"""
测试Django URL配置
"""

import os
import sys
import django
from django.urls import reverse
from django.test import Client

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_project.settings")

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 配置Django
django.setup()


def test_urls():
    """测试URL配置"""
    client = Client()

    print("🔍 测试URL配置...")

    # 测试主页
    try:
        response = client.get("/")
        print(f"✅ 主页 (/): {response.status_code}")
    except Exception as e:
        print(f"❌ 主页 (/): {e}")

    # 测试历史页面
    try:
        response = client.get("/history/")
        print(f"✅ 历史页面 (/history/): {response.status_code}")
    except Exception as e:
        print(f"❌ 历史页面 (/history/): {e}")

    # 测试API端点
    try:
        response = client.get("/api/finance/records/")
        print(f"✅ API记录列表 (/api/finance/records/): {response.status_code}")
    except Exception as e:
        print(f"❌ API记录列表 (/api/finance/records/): {e}")

    # 测试API上传端点
    try:
        response = client.options("/api/finance/records/upload/")
        print(f"✅ API上传端点 (/api/finance/records/upload/): {response.status_code}")
    except Exception as e:
        print(f"❌ API上传端点 (/api/finance/records/upload/): {e}")


if __name__ == "__main__":
    test_urls()
