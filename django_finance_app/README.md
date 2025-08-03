# 财务 Excel 处理系统

基于 Django 的财务 Excel 文件处理 Web 应用，将原始的 Python 脚本改造为现代化的 Web API 系统。

## 功能特性

- 🔄 **Excel 文件上传处理**: 支持拖拽上传，自动解析 Excel 文件
- 📊 **实时处理进度**: 显示处理状态和详细日志
- ⬇️ **结果下载**: 一键下载处理后的 Excel 文件
- 📝 **历史记录**: 查看所有处理历史和详细日志
- 🎨 **现代化界面**: 基于 Bootstrap 5 的响应式设计
- 🔌 **REST API**: 提供完整的 RESTful API 接口

## 技术栈

- **后端**: Django 4.2 + Django REST Framework
- **前端**: Bootstrap 5 + 原生 JavaScript
- **数据库**: SQLite (可轻松切换到 PostgreSQL/MySQL)
- **文件处理**: openpyxl + xlsxwriter

## 快速开始

### 1. 安装依赖

```bash
cd django_finance_app
pip install -r requirements.txt
```

### 2. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

### 4. 启动开发服务器

```bash
python manage.py runserver
```

### 5. 访问应用

- 主页面: http://127.0.0.1:8000/
- 历史记录: http://127.0.0.1:8000/history/
- 管理后台: http://127.0.0.1:8000/admin/
- API 文档: http://127.0.0.1:8000/api/finance/

## API 接口

### 文件上传处理

```
POST /api/finance/records/upload/
Content-Type: multipart/form-data

参数:
- file: Excel文件 (.xlsx, .xls)

响应:
{
  "id": 1,
  "status": "completed",
  "message": "文件处理成功，共处理 10 条记录",
  "output_filename": "排单_20250802_143022.xlsx",
  "processing_time": 2.34,
  "total_records": 10
}
```

### 获取历史记录

```
GET /api/finance/records/

查询参数:
- status: 过滤状态 (pending/completed/failed)
- page: 页码

响应:
{
  "count": 100,
  "next": "http://127.0.0.1:8000/api/finance/records/?page=2",
  "previous": null,
  "results": [...]
}
```

### 下载结果文件

```
GET /api/finance/records/{id}/download/

响应: 文件下载
```

### 获取处理日志

```
GET /api/finance/records/{id}/logs/

响应:
[
  {
    "id": 1,
    "timestamp_display": "2025-08-02 14:30:22",
    "level": "INFO",
    "message": "文件上传成功: 排单.xlsx"
  }
]
```

## 项目结构

```
django_finance_app/
├── manage.py                    # Django管理脚本
├── requirements.txt             # 项目依赖
├── t_Schema.json               # Schema配置文件
├── finance_project/            # Django项目设置
│   ├── __init__.py
│   ├── settings.py             # 项目配置
│   ├── urls.py                 # 主URL路由
│   ├── wsgi.py                 # WSGI配置
│   └── asgi.py                 # ASGI配置
├── finance_app/                # 主应用
│   ├── __init__.py
│   ├── admin.py                # 管理后台配置
│   ├── apps.py                 # 应用配置
│   ├── models.py               # 数据模型
│   ├── serializers.py          # API序列化器
│   ├── views.py                # 视图/API端点
│   ├── urls.py                 # 应用URL路由
│   ├── migrations/             # 数据库迁移文件
│   └── services/               # 业务逻辑层
│       ├── __init__.py
│       └── excel_processor.py  # Excel处理核心逻辑
├── templates/                  # HTML模板
│   ├── index.html              # 主页面
│   └── history.html            # 历史记录页面
├── static/                     # 静态文件
├── media/                      # 媒体文件存储
│   ├── uploads/                # 上传文件目录
│   └── outputs/                # 输出文件目录
└── db.sqlite3                  # SQLite数据库文件
```

## 核心特性说明

### 1. 文件上传与处理

- 支持拖拽上传和点击上传
- 自动验证文件格式和大小
- 异步处理，显示实时进度
- 详细的错误处理和用户反馈

### 2. 数据处理逻辑

- 保持原有的 Excel 处理逻辑不变
- 解析多个工作表：付款数据、供应商、项目、费用代码
- 自动映射字段和生成财务记录
- 支持不同付款类型的处理规则

### 3. 历史记录管理

- 分页显示处理历史
- 支持状态过滤和日期范围查询
- 详细的处理日志查看
- 一键下载历史结果文件

### 4. REST API 设计

- 遵循 RESTful 设计原则
- 完整的 CRUD 操作支持
- 统一的错误处理
- JSON 格式的数据交换

## 部署说明

### 开发环境

- 使用 `python manage.py runserver` 启动
- DEBUG = True，包含详细错误信息
- 使用 SQLite 数据库

### 生产环境建议

1. 设置 `DEBUG = False`
2. 配置生产级数据库（PostgreSQL/MySQL）
3. 配置静态文件服务（nginx/Apache）
4. 使用 WSGI 服务器（gunicorn/uWSGI）
5. 配置日志文件轮转
6. 设置合适的文件上传大小限制

## 维护与扩展

### 添加新的处理规则

1. 修改 `finance_app/services/excel_processor.py`
2. 更新相关的映射配置
3. 添加相应的单元测试

### 扩展 API 功能

1. 在 `views.py` 中添加新的端点
2. 创建对应的序列化器
3. 更新 URL 路由配置

### 自定义前端界面

1. 修改 `templates/` 中的 HTML 文件
2. 添加自定义 CSS/JS 到 `static/` 目录
3. 使用 Django 模板系统进行动态渲染

## 故障排除

### 常见问题

1. **文件上传失败**: 检查文件大小限制和格式
2. **处理错误**: 查看详细日志和错误信息
3. **权限问题**: 确保 media 目录有写入权限
4. **端口占用**: 更改运行端口或停止占用进程

### 日志查看

- 应用日志: `finance_app.log`
- Django 日志: 控制台输出
- 处理日志: 通过 Web 界面查看

## 联系支持

如有问题或建议，请提交 Issue 或联系开发团队。
