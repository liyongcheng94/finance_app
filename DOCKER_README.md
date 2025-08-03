# Docker Compose 使用指南

## 环境配置

本项目支持开发环境和生产环境的 Docker 部署。

### 1. 环境文件配置

首先复制环境变量模板：

```bash
# 开发环境
cp .env.dev .env

# 生产环境
cp .env.example .env
```

然后根据你的实际情况修改 `.env` 文件中的配置。

### 2. 开发环境部署

开发环境使用 SQLite 数据库，包含热重载功能：

```bash
# 构建并启动开发环境
docker-compose -f docker-compose.dev.yml up --build

# 后台运行
docker-compose -f docker-compose.dev.yml up -d --build
```

开发环境特性：

- 使用 SQLite 数据库（简单快速）
- 代码热重载
- Debug 模式开启
- 自动创建开发用户：`dev/dev123`
- 访问地址：http://localhost:8000

### 3. 生产环境部署

生产环境使用 PostgreSQL + Redis + Nginx：

```bash
# 构建并启动生产环境
docker-compose up --build

# 后台运行
docker-compose up -d --build
```

生产环境特性：

- PostgreSQL 数据库
- Redis 缓存
- Nginx 反向代理
- Gunicorn WSGI 服务器
- 自动创建管理员用户：`admin/admin123`
- 访问地址：http://localhost

### 4. 常用命令

```bash
# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据卷（注意：会丢失数据）
docker-compose down -v

# 重建服务
docker-compose up --build --force-recreate

# 进入 Django 容器
docker-compose exec web bash

# 运行 Django 管理命令
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic
```

### 5. 数据备份与恢复

#### PostgreSQL 数据备份：

```bash
# 备份数据库
docker-compose exec db pg_dump -U financeuser financedb > backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
docker-compose exec -T db psql -U financeuser financedb < backup_file.sql
```

#### 文件备份：

```bash
# 备份上传文件和输出文件
docker cp $(docker-compose ps -q web):/app/media ./media_backup_$(date +%Y%m%d_%H%M%S)
```

### 6. 环境变量说明

主要环境变量：

- `DEBUG`: 是否开启调试模式
- `SECRET_KEY`: Django 密钥
- `DATABASE_URL`: 数据库连接字符串
- `REDIS_URL`: Redis 连接字符串
- `ALLOWED_HOSTS`: 允许的主机列表
- `DEFAULT_PREPARED_BY`: 默认制表人

### 7. 端口说明

- **开发环境**：8000 (Django 开发服务器)
- **生产环境**：80 (Nginx)
- **PostgreSQL**：5432 (仅内部访问)
- **Redis**：6379 (仅内部访问)

### 8. 故障排除

#### 常见问题：

1. **端口冲突**：

   ```bash
   # 检查端口占用
   netstat -tulpn | grep :80
   # 修改 docker-compose.yml 中的端口映射
   ```

2. **权限问题**：

   ```bash
   # 给脚本执行权限
   chmod +x entrypoint.sh entrypoint.dev.sh
   ```

3. **数据库连接失败**：

   ```bash
   # 检查数据库容器状态
   docker-compose logs db
   # 重启数据库服务
   docker-compose restart db
   ```

4. **静态文件问题**：
   ```bash
   # 重新收集静态文件
   docker-compose exec web python manage.py collectstatic --noinput
   ```

### 9. 开发建议

1. 开发时使用 `docker-compose.dev.yml`
2. 生产部署前测试 `docker-compose.yml`
3. 定期备份生产数据
4. 监控容器资源使用情况
5. 及时更新环境变量配置

### 10. 安全注意事项

1. 生产环境必须修改默认密码
2. 使用强密码和随机 SECRET_KEY
3. 配置防火墙和 SSL 证书
4. 定期更新 Docker 镜像
5. 监控访问日志
