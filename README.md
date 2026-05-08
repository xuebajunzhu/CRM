# Django CRM System

[![CI/CD](https://github.com/yourusername/django-crm/actions/workflows/deploy.yml/badge.svg)](https://github.com/yourusername/django-crm/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

一个功能完整的客户关系管理 (CRM) 系统，基于 Django 构建，支持客户管理、咨询跟踪、学习记录等功能。

## ✨ 特性

### 🛡️ 安全性
- ✅ PBKDF2 密码加密 (Django 内置)
- ✅ CSRF/XSS 防护
- ✅ SQL 注入防护
- ✅ 会话安全管理
- ✅ 环境变量配置
- ✅ 安全日志记录

### 📋 功能模块
- 👥 **用户管理**: 多角色权限控制
- 🏢 **部门管理**: 组织架构管理
- 🏫 **校区管理**: 多校区支持
- 👨‍🎓 **班级管理**: 课程班级分配
- 💼 **客户管理**: 潜在客户跟踪
- 📞 **咨询记录**: 销售咨询跟进
- 📚 **学习记录**: 学员学习进度
- 📊 **数据仪表盘**: 可视化统计分析

### 🎨 用户体验
- 📱 **响应式设计**: 完美支持移动端
- ⚡ **实时验证**: 表单即时反馈
- 🎬 **动画效果**: 流畅的过渡动画
- 🔔 **友好提示**: 清晰的错误信息
- 🌙 **现代 UI**: 简洁美观的界面

### 🚀 部署与运维
- 🔄 **CI/CD**: GitHub Actions 自动测试部署
- ☁️ **云部署**: Render.com 一键部署
- 🗄️ **数据库**: PostgreSQL/MySQL/SQLite 支持
- 📦 **容器化**: Docker 支持 (可选)
- 📈 **监控**: 日志和性能监控

## 🚀 快速开始

### 本地开发

#### 1. 克隆项目
```bash
git clone https://github.com/yourusername/django-crm.git
cd django-crm
```

#### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

#### 3. 安装依赖
```bash
pip install -r requirements.txt
```

#### 4. 配置环境变量
```bash
cp .env.example .env
# 编辑 .env 文件，设置 SECRET_KEY 等配置
```

#### 5. 数据库迁移
```bash
cd CRM01
python manage.py makemigrations
python manage.py migrate
```

#### 6. 加载测试数据 (可选)
```bash
python manage.py dbshell < ../data/test_data.sql
```

#### 7. 创建超级用户
```bash
python manage.py createsuperuser
# 或使用默认账号：admin / admin123 (仅限测试环境)
```

#### 8. 运行开发服务器
```bash
python manage.py runserver
```

#### 9. 访问系统
```
http://127.0.0.1:8000/
```

## 📁 项目结构

```
django-crm/
├── CRM01/                  # 项目主配置目录
│   ├── settings.py         # Django 配置
│   ├── urls.py             # 主 URL 路由
│   └── wsgi.py             # WSGI 配置
├── app01/                  # 主要应用模块
│   ├── models.py           # 数据模型
│   ├── views/              # 视图函数
│   ├── urls.py             # 应用 URL 路由
│   ├── forms.py            # 表单定义
│   └── admin.py            # Admin 配置
├── statics/                # 静态文件
│   ├── css/                # 样式表
│   ├── js/                 # JavaScript
│   └── images/             # 图片资源
├── templates/              # HTML 模板
│   ├── base.html           # 基础模板
│   ├── dashboard.html      # 仪表盘
│   └── login.html          # 登录页
├── data/                   # 测试数据
│   └── test_data.sql       # SQL 测试数据
├── scripts/                # 工具脚本
│   └── generate_test_data.py
├── .github/workflows/      # GitHub Actions
├── .env.example            # 环境变量示例
├── .gitignore              # Git 忽略规则
├── build.sh                # 构建脚本
├── render.yaml             # Render 部署配置
├── requirements.txt        # Python 依赖
├── README.md               # 本文件
└── DEPLOY.md               # 部署指南
```

## 🛠️ 技术栈

- **后端框架**: Django 3.2 LTS
- **数据库**: SQLite3 (开发) / PostgreSQL (生产)
- **前端**: HTML5, CSS3, JavaScript (原生)
- **Web 服务器**: Gunicorn
- **部署平台**: Render.com
- **CI/CD**: GitHub Actions

## 📋 主要功能

### 客户管理
- 客户信息录入与维护
- 客户分类与标签
- 客户分配与跟进
- 客户状态跟踪

### 销售流程
- 咨询记录管理
- 销售机会跟踪
- 转化漏斗分析
- 业绩统计报表

### 教学管理
- 班级与课程管理
- 学员学习记录
- 作业提交与批改
- 考勤管理

### 系统管理
- 用户与权限管理
- 部门与校区管理
- 操作日志审计
- 数据备份恢复

## 🌐 云部署

本项目支持一键部署到 Render.com，详见 [部署指南](DEPLOY.md)。

### 快速部署步骤

1. Fork 本项目到你的 GitHub 账号
2. 在 [Render.com](https://render.com) 注册账号
3. 点击 "New +" → "Web Service"
4. 选择你的 GitHub 仓库
5. 使用以下配置：
   - Build Command: `./build.sh`
   - Start Command: `gunicorn CRM01.wsgi:application`
6. 添加 PostgreSQL 数据库
7. 配置环境变量
8. 部署完成！

详细步骤请参考 [DEPLOY.md](DEPLOY.md)。

## 🧪 测试

### 运行单元测试
```bash
cd CRM01
python manage.py test
```

### 运行代码检查
```bash
flake8 .
pylint app01/
```

### 测试覆盖率
```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 API 文档

RESTful API 文档将在后续版本中提供 (计划集成 Django REST Framework)。

## 🔐 安全说明

### 默认账户 (仅测试环境)
- 用户名：`admin`
- 密码：`admin123`

**⚠️ 重要**: 生产环境请务必修改默认密码！

### 安全最佳实践
1. 使用强密码策略
2. 定期更新依赖包
3. 启用 HTTPS
4. 配置防火墙规则
5. 定期备份数据库
6. 监控异常登录

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发流程
1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 代码规范
- 遵循 PEP 8 编码规范
- 添加必要的注释和文档字符串
- 编写单元测试覆盖新功能

## 📝 更新日志

### v2.0.0 (2024)
- ✅ 升级到 Django 3.2 LTS
- ✅ 密码加密升级为 PBKDF2
- ✅ 添加响应式设计
- ✅ 实现数据可视化仪表盘
- ✅ 集成 CI/CD 流水线
- ✅ 支持云部署

### v1.0.0 (2017)
- 初始版本发布

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 📞 联系方式

- 📧 Email: your.email@example.com
- 💬 Issues: [GitHub Issues](https://github.com/yourusername/django-crm/issues)
- 📖 Wiki: [项目 Wiki](https://github.com/yourusername/django-crm/wiki)

## 🙏 致谢

感谢所有贡献者和使用者！

---

**注意**: 本项目仅供学习和内部使用。生产环境部署前请进行充分的安全评估和测试。
