#!/bin/bash

# Finance App - Ubuntu 一键启动脚本
# 作者: 自动生成
# 日期: 2025-08-02
# 说明: 用于在Ubuntu系统上快速启动Django财务管理应用

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

log_info "正在启动财务管理应用..."
log_info "工作目录: $SCRIPT_DIR"

# 检查Python环境
check_python() {
    log_info "检查Python环境..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_success "Python版本: $PYTHON_VERSION"
        PYTHON_CMD="python3"
        elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2)
        log_success "Python版本: $PYTHON_VERSION"
        PYTHON_CMD="python"
    else
        log_error "未找到Python，请先安装Python 3.8+"
        exit 1
    fi
}

# 检查pip环境
check_pip() {
    log_info "检查pip环境..."
    
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        log_error "未找到pip，请先安装pip"
        exit 1
    fi
    log_success "pip环境检查完成"
}

# 检查虚拟环境
setup_venv() {
    log_info "检查虚拟环境..."
    
    if [ ! -d "venv" ]; then
        log_warning "虚拟环境不存在，正在创建..."
        $PYTHON_CMD -m venv venv
        log_success "虚拟环境创建完成"
    fi
    
    # 激活虚拟环境
    log_info "激活虚拟环境..."
    source venv/bin/activate
    log_success "虚拟环境已激活"
}

# 安装依赖
install_dependencies() {
    log_info "检查并安装依赖包..."
    
    if [ -f "requirements.txt" ]; then
        log_info "正在安装requirements.txt中的依赖..."
        pip install -r requirements.txt
        log_success "依赖安装完成"
    else
        log_warning "未找到requirements.txt，手动安装基本依赖..."
        pip install Django>=4.0,\<5.0 djangorestframework>=3.14.0 openpyxl>=3.1.0 xlsxwriter>=3.1.0 django-cors-headers>=4.0.0
        log_success "基本依赖安装完成"
    fi
}

# 数据库迁移
migrate_database() {
    log_info "执行数据库迁移..."
    
    if [ -f "manage.py" ]; then
        $PYTHON_CMD manage.py makemigrations
        $PYTHON_CMD manage.py migrate
        log_success "数据库迁移完成"
    else
        log_error "未找到manage.py文件"
        exit 1
    fi
}

# 收集静态文件
collect_static() {
    log_info "收集静态文件..."
    
    # 检查是否需要收集静态文件
    if grep -q "STATIC_ROOT" finance_project/settings.py 2>/dev/null; then
        $PYTHON_CMD manage.py collectstatic --noinput
        log_success "静态文件收集完成"
    else
        log_info "跳过静态文件收集（开发模式）"
    fi
}

# 启动服务器
start_server() {
    log_info "启动Django开发服务器..."
    
    # 获取本机IP地址
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    
    echo ""
    log_success "==================== 服务器启动成功 ===================="
    log_success "本地访问地址: http://127.0.0.1:8000"
    log_success "局域网访问地址: http://$LOCAL_IP:8000"
    log_success "管理后台: http://127.0.0.1:8000/admin/"
    log_success "API接口: http://127.0.0.1:8000/api/"
    log_success "======================================================="
    echo ""
    log_info "按 Ctrl+C 停止服务器"
    echo ""
    
    # 启动服务器
    $PYTHON_CMD manage.py runserver 0.0.0.0:8000
}

# 主函数
main() {
    echo ""
    log_info "======================================================="
    log_info "    财务管理应用 - Ubuntu 一键启动脚本"
    log_info "======================================================="
    echo ""
    
    check_python
    check_pip
    setup_venv
    install_dependencies
    migrate_database
    collect_static
    start_server
}

# 错误处理
trap 'log_error "启动过程中发生错误，请检查上述日志"; exit 1' ERR

# 执行主函数
main "$@"
# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
fi

# 快速数据库迁移
if [ -f "manage.py" ]; then
    echo "检查数据库迁移..."
    python manage.py migrate --run-syncdb 2>/dev/null || python manage.py migrate
fi

# 获取本机IP
LOCAL_IP=$(hostname -I | awk '{print $1}' 2>/dev/null || echo "localhost")

echo ""
echo -e "${GREEN}==================== 服务启动 ====================${NC}"
echo -e "${GREEN}本地地址: http://127.0.0.1:8000${NC}"
echo -e "${GREEN}局域网地址: http://$LOCAL_IP:8000${NC}"
echo -e "${GREEN}===============================================${NC}"
echo ""

# 启动服务器
python manage.py runserver 0.0.0.0:8000
