# 使用官方Python运行时作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONPATH=/app \
  DJANGO_SETTINGS_MODULE=finance_project.settings

# 安装系统依赖
RUN apt-get update && apt-get install -y \
  build-essential \
  libpq-dev \
  netcat-traditional \
  && rm -rf /var/lib/apt/lists/*

# 复制requirements文件
COPY django_finance_app/requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY django_finance_app/ .

# 创建必要的目录
RUN mkdir -p media/uploads media/outputs static logs

# 设置权限
RUN chmod -R 755 media static logs

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE 8000

# 复制启动脚本
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# 启动命令
CMD ["/app/entrypoint.sh"]
