"""
测试Django项目设置
"""

import os
import sys
import django

# 设置Django环境
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_project.settings")

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 配置Django
django.setup()

# 测试导入
try:
    from finance_app.models import FinanceRecord, ProcessingLog
    from finance_app.services.excel_processor import ExcelProcessor

    print("✅ Django项目配置正确")
    print("✅ 模型导入成功")
    print("✅ Excel处理器导入成功")

    # 测试Excel处理器
    processor = ExcelProcessor()
    print("✅ Excel处理器实例化成功")

    print("\n🎉 所有测试通过！项目配置正确。")
    print("\n📝 下一步操作:")
    print("1. 运行: python manage.py makemigrations")
    print("2. 运行: python manage.py migrate")
    print("3. 运行: python manage.py runserver")
    print("4. 访问: http://127.0.0.1:8000/")

except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请检查依赖包是否正确安装")
except Exception as e:
    print(f"❌ 配置错误: {e}")
    print("请检查Django项目配置")
