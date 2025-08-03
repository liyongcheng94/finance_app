@echo off
chcp 65001
echo.
echo ========================================
echo    财务Excel处理系统 - 简化启动版
echo ========================================
echo.

cd /d %~dp0

echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [2/3] 安装必要依赖...
echo 安装Django...
python -m pip install Django --quiet

echo 安装其他依赖...
python -m pip install djangorestframework --quiet
python -m pip install openpyxl --quiet  
python -m pip install xlsxwriter --quiet
python -m pip install django-cors-headers --quiet

echo [3/3] 初始化并启动...
python manage.py makemigrations finance_app 2>nul
python manage.py migrate 2>nul

echo.
echo ========================================
echo 🚀 正在启动服务器...
echo.
echo 🌐 主页面: http://127.0.0.1:8000/
echo 📊 历史记录: http://127.0.0.1:8000/history/
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python manage.py runserver 0.0.0.0:8000
