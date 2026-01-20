# Django后端项目

## 技术栈
- Django 4.2+
- Django REST Framework
- SQLite (可配置其他数据库)
- JWT认证

## 安装步骤

1. 创建虚拟环境
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

4. 创建超级用户
```bash
python manage.py createsuperuser
```

5. 运行开发服务器
```bash
python manage.py runserver
```

## API端点

### 认证
- POST /api/auth/login/ - 用户登录
- POST /api/auth/register/ - 用户注册
- POST /api/auth/refresh/ - 刷新token

### 仓库管理
- GET/POST /api/warehouse/items/ - 物品列表/添加
- GET/PUT/DELETE /api/warehouse/items/{id}/ - 物品详情/更新/删除
- GET /api/warehouse/stock/ - 当前库存
- POST /api/warehouse/inbound/ - 入库记录
- POST /api/warehouse/outbound/ - 出库记录

### 用户管理
- GET/POST /api/users/ - 用户列表/创建
- GET/PUT/DELETE /api/users/{id}/ - 用户详情/更新/删除

## 项目结构
```
backend/
├── config/          # 项目配置
├── apps/
│   ├── warehouse/   # 仓库管理应用
│   ├── users/       # 用户管理应用
│   └── system/      # 系统管理应用
├── manage.py
└── requirements.txt
```
