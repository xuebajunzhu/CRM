# CRM 客户关系管理系统

基于 Django 开发的 CRM（Customer Relationship Management）客户关系管理系统。

## 项目结构

```
├── CRM01/              # 项目主配置目录
├── app01/              # 主要应用模块
│   ├── MyModelForm/    # ModelForm 相关
│   ├── mymiddlewares/  # 自定义中间件
│   ├── templatetags/   # 模板标签
│   └── views/          # 视图函数
├── statics/            # 静态文件 (CSS, JS, 图片等)
├── templates/          # HTML 模板文件
├── utils/              # 工具函数模块
├── manage.py           # Django 项目管理脚本
├── db.sqlite3          # SQLite 数据库文件
└── virtualenv.txt      # 项目依赖包列表
```

## 技术栈

- **后端框架**: Django
- **数据库**: SQLite3
- **前端**: HTML, CSS, JavaScript
- **其他依赖**: 见 `virtualenv.txt`

## 主要功能

- 客户信息管理
- 销售跟踪
- 数据报表
- 用户权限管理

## 安装与运行

### 环境要求

- Python 3.x
- pip

### 安装步骤

1. 克隆项目
```bash
git clone <repository-url>
cd <project-directory>
```

2. 创建虚拟环境（可选）
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. 安装依赖
```bash
pip install django
# 其他依赖参考 virtualenv.txt
```

4. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

5. 创建超级用户
```bash
python manage.py createsuperuser
```

6. 运行开发服务器
```bash
python manage.py runserver
```

7. 访问系统
```
http://127.0.0.1:8000/
```

## 目录说明

- `app01/`: 核心业务逻辑模块
  - `models.py`: 数据模型定义
  - `urls.py`: URL 路由配置
  - `views/`: 视图处理
  - `admin.py`: Django Admin 配置
  
- `templates/`: HTML 模板文件
- `statics/`: 静态资源文件
- `utils/`: 通用工具函数

## 开发说明

### 添加新的 Model

1. 在 `app01/models.py` 中定义模型类
2. 执行 `python manage.py makemigrations`
3. 执行 `python manage.py migrate`

### 添加新的 View

1. 在 `app01/views/` 目录下创建视图函数
2. 在 `app01/urls.py` 中配置 URL 路由

## 许可证

本项目仅供学习和内部使用。

## 联系方式

如有问题，请联系开发团队。
