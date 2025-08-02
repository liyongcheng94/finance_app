@echo off
chcp 65001
echo.
echo ========================================
echo    财务Excel处理系统 - Django版
echo ========================================
echo.

cd /d %~dp0

echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

echo [2/4] 安装依赖包...
echo 正在逐个安装核心依赖包，这可能需要几分钟...
pip install Django==4.2.7
if errorlevel 1 (
    echo 警告：Django安装失败，尝试其他版本...
    pip install Django
)

pip install djangorestframework
if errorlevel 1 (
    echo 警告：DRF安装失败，尝试继续...
)

pip install django-cors-headers
pip install openpyxl
pip install xlsxwriter

echo 依赖包安装完成（部分警告可忽略）

echo [3/4] 初始化数据库...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo 错误：数据库初始化失败
    pause
    exit /b 1
)

echo [4/4] 启动服务器...
echo.
echo ========================================
echo 服务器启动成功！
echo.
echo 🌐 主页面: http://127.0.0.1:8000/
echo 📊 历史记录: http://127.0.0.1:8000/history/
echo ⚙️  管理后台: http://127.0.0.1:8000/admin/
echo 🔌 API接口: http://127.0.0.1:8000/api/finance/
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python manage.py runserver
