# Deploy Django CRM to Render.com

## 📋 前提条件

1. GitHub 账号
2. Render.com 账号 (免费)
3. 项目已推送到 GitHub

## 🚀 部署步骤

### 方法一：使用 Render Dashboard (推荐)

#### 1. 连接 GitHub 仓库
- 登录 [Render.com](https://render.com)
- 点击 "New +" → "Web Service"
- 选择你的 GitHub 仓库

#### 2. 配置服务
```
Name: django-crm-system
Region: Oregon (或选择最近的)
Branch: main
Root Directory: (留空)
Runtime: Python
Build Command: ./build.sh
Start Command: gunicorn CRM01.wsgi:application
Instance Type: Free
```

#### 3. 添加环境变量
在 Render Dashboard 中添加以下变量：

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.9.0` |
| `SECRET_KEY` | (点击 Generate 生成随机值) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `<your-app-name>.onrender.com` |
| `WEB_CONCURRENCY` | `4` |

#### 4. 创建数据库
- 在 Render Dashboard 点击 "New +" → "PostgreSQL"
- 配置：
  ```
  Name: crm-db
  Database: crm_db
  Plan: Free
  ```
- 复制 Connection String (Internal Database URL)

#### 5. 关联数据库
- 在 Web Service 的环境变量中添加：
  ```
  DATABASE_URL: <从 PostgreSQL 服务复制的 Internal URL>
  ```

#### 6. 部署
- 保存配置后，Render 会自动开始构建和部署
- 查看部署日志确认成功

### 方法二：使用 render.yaml (Infrastructure as Code)

#### 1. 确保 render.yaml 已提交
本项目已包含 `render.yaml` 配置文件

#### 2. 通过 CLI 部署
```bash
# 安装 Render CLI
npm install -g @render-cloud/render-cli

# 登录
render login

# 部署
render up
```

## 🔐 安全配置

### GitHub Secrets 设置
如果使用 GitHub Actions 自动部署，需要在 GitHub 仓库设置 Secrets：

1. 进入 GitHub 仓库 → Settings → Secrets and variables → Actions
2. 添加以下 secrets：

```
RENDER_API_KEY: <从 Render Dashboard 获取>
RENDER_SERVICE_ID: <服务 ID>
```

### 获取 Render API Key
1. 登录 Render Dashboard
2. 点击右上角头像 → Account Settings
3. 滚动到 "API Keys" 部分
4. 点击 "Create API Key"

## 📊 验证部署

### 1. 访问应用
```
https://<your-app-name>.onrender.com
```

### 2. 测试登录
- 用户名：`admin`
- 密码：`admin123`

### 3. 检查数据库
在 Render Dashboard 的 PostgreSQL 页面可以查看数据库状态

## 🔧 常见问题

### 静态文件不加载
确保 `build.sh` 中包含 `collectstatic` 命令，本项目的 build.sh 已配置

### 数据库迁移失败
检查 `DATABASE_URL` 是否正确配置

### 构建超时
Free 计划有构建时间限制，如超时请优化依赖或升级到付费计划

### 应用启动慢
首次访问时 Free 实例会休眠，需要 30-50 秒冷启动时间

## 📈 监控和日志

### 查看日志
- Render Dashboard → Services → 选择服务 → Logs
- 实时查看应用日志

### 性能监控
- Render Dashboard 提供基本的 CPU 和内存使用率
- 建议集成 Sentry 进行错误追踪

## 🔄 持续部署

每次推送到 `main` 分支时，Render 会自动重新部署：

```bash
git push origin main
```

GitHub Actions 也会运行测试并触发部署（如果配置了）

## 💰 成本估算

### Free 计划
- Web Service: $0/月 (每月 750 小时实例时间)
- PostgreSQL: $0/月 (前 90 天免费，之后 $7/月)
- 带宽: 前 100GB 免费

### 预估月度成本
- 开发/测试环境: $0-7
- 生产环境 (升级实例): $7-25

## 🎯 下一步优化

1. **启用 HTTPS**: Render 自动提供 SSL 证书
2. **自定义域名**: 在 Render Dashboard 配置
3. **备份数据库**: 设置自动备份策略
4. **性能优化**: 添加 Redis 缓存
5. **监控告警**: 集成 Uptime Robot 等监控服务

## 📞 支持资源

- [Render 文档](https://render.com/docs)
- [Django 部署指南](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Gunicorn 配置](https://docs.gunicorn.org/en/stable/configure.html)

---

**注意**: 首次部署后，请务必修改默认管理员密码！
