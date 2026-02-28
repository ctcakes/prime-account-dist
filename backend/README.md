# Prime Account Dist - Backend

Flask 后端服务，用于账号分发链接管理。

## 功能特性

- 创建账号分发链接
- 链接访问和账号获取
- 链接状态检查
- 自动过期清理
- SQLite 数据存储

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动

## API 接口

### 创建链接
- POST `/api/create`
- 参数: `accounts` (账号列表), `expire_hours` (有效期小时数)
- 返回: `uuid`, `link`

### 获取链接内容
- GET `/api/link/<uuid>`
- 返回: 账号列表或过期状态

### 检查状态
- GET `/api/status/<uuid>`
- 返回: 链接状态和剩余时间

### 失效链接
- DELETE `/api/link/<uuid>`
- 返回: 成功信息

## 数据库

使用 SQLite，自动创建 `account_links` 表。