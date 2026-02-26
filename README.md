# 银行系统示例（Django + MySQL + MongoDB + Minio）

本项目是在当前目录下创建的示例银行系统，使用：

- **后端框架**：Django 3.2 LTS（Python）
- **关系型数据库**：MySQL（用于核心账户、交易等业务数据）
- **文档数据库**：MongoDB（通过 Djongo，用于审计日志等非结构化数据）
- **对象存储**：Minio（用于存储对账单、附件等文件）

## 快速开始

1. **安装依赖（本地开发）**

```bash
pip install -r requirements.txt
```

2. **配置数据库与 Minio**

在 `bank_project/settings.py` 中修改：

- MySQL 连接信息（`DATABASES['default']`）
- MongoDB 连接信息（`DATABASES['mongo']`，Djongo）
- Minio 访问配置（`MINIO_*` 相关配置）

3. **数据库迁移**

```bash
python manage.py makemigrations banking audit
python manage.py migrate
```

4. **运行开发服务器（本地开发方式）**

```bash
python manage.py runserver
```

启动后访问 `http://127.0.0.1:8000/`，可以看到简易的银行系统演示界面（账户列表 / 简单交易 / 对账单上传）。

5. **使用 Docker 一键启动（推荐）**

```bash
docker compose build --no-cache web    # 首次或修改 requirements.txt 后建议加 --no-cache
docker compose up -d                   # 启动 MySQL + MongoDB + Minio + Web
docker compose run --rm web python manage.py migrate
docker compose run --rm web python manage.py createsuperuser
```

然后访问：

- `http://localhost:8000/`：前台银行系统
- `http://localhost:8000/admin/`：Django 后台管理
- `http://localhost:9001/`：Minio 控制台（默认账号/密码：`minioadmin` / `minioadmin`）

### 初始化业务数据

1. 打开 `http://localhost:8000/admin/`，使用超级用户登录。  
2. 在 `Customers` 中新建客户。  
3. 在 `Accounts` 中为客户创建账户（账号、账户类型、初始余额等）。  
4. 返回前台首页，在账户卡片中可以：
   - 点击“对该账户交易”创建交易；
   - 点击“上传对账单”上传该账户的对账单文件。

## 功能概览

- **账户管理**（MySQL）：客户、账户、余额字段等。
- **交易记录**（MySQL）：存款 / 取款 / 转账等基础交易，并在前台页面发起。
- **审计日志**（MongoDB + Djongo）：每次交易、对账单上传都会写入 `AuditLog`，存储在 MongoDB。
- **对账单上传**（Minio）：在账户卡片点击“上传对账单”，文件会保存到 Minio 对象存储，并在 MySQL 中记录元数据。

> 提示：每次交易和对账单上传，都会在 MongoDB 中写入一条 `AuditLog` 记录，便于审计追踪。

## 常见问题

- **访问首页时报错：`ProgrammingError: 表 'bank_db.banking_account' 不存在`**
  - 说明当前 MySQL 实例还没有应用迁移。请执行：
    - 本地：`python manage.py makemigrations banking audit && python manage.py migrate`
    - Docker：`docker compose run --rm web python manage.py makemigrations banking audit && docker compose run --rm web python manage.py migrate`
- **Docker 构建时依赖冲突（Django 与 Djongo）**
  - 已在 `requirements.txt` 中固定为兼容组合：`Django 3.2.25 + Djongo 1.3.6 + sqlparse 0.2.4`，若你修改依赖，请确保版本兼容并使用 `docker compose build --no-cache web` 重新构建。

## 目录结构（核心部分）

- `manage.py`：Django 管理脚本
- `bank_project/`：Django 项目配置（settings/urls 等）
- `banking/`：银行核心业务（账户、交易、对账单上传等，使用 MySQL）
- `audit/`：审计日志与操作记录（使用 MongoDB + Djongo）
- `storage/`：Minio 客户端封装与文件上传接口
- `docker-compose.yml`：一键启动 MySQL + MongoDB + Minio + Web 的编排文件
- `Dockerfile`：Web 应用容器构建配置

本项目只是一个**教学/示例**骨架，方便你在此基础上扩展成完整的银行业务系统（例如增加权限/角色、对账单下载、API 网关等）。

