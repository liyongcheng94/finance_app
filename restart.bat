@echo off
chcp 65001
echo.
echo ========================================
echo    重启Django服务器
echo ========================================
echo.

cd /d %~dp0

echo 正在重启服务器...
echo.
echo 🌐 访问地址:
echo   - 主页: http://127.0.0.1:8000/
echo   - 历史记录: http://127.0.0.1:8000/history/
echo   - API上传: http://127.0.0.1:8000/api/finance/records/upload/
echo.
echo 按 Ctrl+C 停止服务器
echo ========================================
echo.

python manage.py runserver
