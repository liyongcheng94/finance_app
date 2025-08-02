# Ubuntu 部署指南

本文档说明如何在 Ubuntu 系统上部署和运行财务管理应用。

## 🚀 快速开始

### 1. 首次部署（推荐）

```bash
# 添加执行权限
chmod +x setup_permissions_ubuntu.sh
./setup_permissions_ubuntu.sh

# 一键启动（自动配置环境）
./start_ubuntu.sh
```

### 2. 日常使用

```bash
# 简化启动（环境已配置）
./start_simple_ubuntu.sh
```

## 📋 脚本说明

### `start_ubuntu.sh` - 完整启动脚本

- ✅ 自动检查 Python 环境
- ✅ 自动创建虚拟环境
- ✅ 自动安装依赖
- ✅ 自动数据库迁移
- ✅ 启动开发服务器
- 🎯 **推荐首次使用**

### `start_simple_ubuntu.sh` - 简化启动脚本

- ✅ 快速启动
- ✅ 基本检查
- ✅ 适合日常使用
- 🎯 **环境已配置时使用**

### `start_production_ubuntu.sh` - 生产环境脚本

- ✅ 使用 Gunicorn 服务器
- ✅ 多进程支持
- ✅ 性能优化
- 🎯 **生产环境使用**

### `install_service_ubuntu.sh` - 系统服务安装

- ✅ 安装为系统服务
- ✅ 开机自启动
- ✅ 后台运行
- 🎯 **服务器部署使用**

## 🔧 环境要求

### 系统要求

- Ubuntu 18.04+ (推荐 20.04+)
- Python 3.8+
- pip

### 自动安装的依赖

- Django >= 4.0
- djangorestframework >= 3.14.0
- openpyxl >= 3.1.0
- xlsxwriter >= 3.1.0
- django-cors-headers >= 4.0.0

## 🌐 访问地址

启动成功后可以通过以下地址访问：

- **本地访问**: http://127.0.0.1:8000
- **局域网访问**: http://你的 IP:8000
- **管理后台**: http://127.0.0.1:8000/admin/
- **API 接口**: http://127.0.0.1:8000/api/

## 🛠️ 手动安装步骤

如果自动脚本遇到问题，可以手动执行：

```bash
# 1. 安装Python和pip
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 5. 启动服务
python manage.py runserver 0.0.0.0:8000
```

## 🔥 生产环境部署

### 使用 Gunicorn

```bash
# 安装Gunicorn
pip install gunicorn

# 启动生产服务器
./start_production_ubuntu.sh
```

### 安装为系统服务

```bash
# 需要root权限
sudo ./install_service_ubuntu.sh

# 管理服务
sudo systemctl start finance-app    # 启动
sudo systemctl stop finance-app     # 停止
sudo systemctl restart finance-app  # 重启
sudo systemctl status finance-app   # 查看状态
sudo journalctl -u finance-app -f   # 查看日志
```

## 🐛 故障排除

### 权限问题

```bash
chmod +x *.sh
```

### Python 版本问题

```bash
# 检查Python版本
python3 --version

# 如果版本过低，安装新版本
sudo apt install python3.9
```

### 端口占用

```bash
# 查看端口占用
sudo netstat -tlnp | grep :8000

# 杀死占用进程
sudo kill -9 PID
```

### 依赖安装失败

```bash
# 更新pip
pip install --upgrade pip

# 手动安装依赖
pip install Django djangorestframework openpyxl xlsxwriter django-cors-headers
```

## 📝 日志文件

- 应用日志: `finance_app.log`
- 系统服务日志: `sudo journalctl -u finance-app`

## 🔒 安全建议

生产环境部署时请注意：

1. 修改 `settings.py` 中的 `DEBUG = False`
2. 设置正确的 `ALLOWED_HOSTS`
3. 配置 HTTPS（使用 Nginx+SSL）
4. 使用生产数据库（PostgreSQL/MySQL）
5. 配置防火墙规则

## 📞 技术支持

如果遇到问题，请检查：

1. 系统要求是否满足
2. 网络连接是否正常
3. 端口是否被占用
4. 权限是否正确

---

**祝您使用愉快！** 🎉
