# Prime Account Dist

CS2 官匹账号安全分发工具

## 项目简介

这是一个用于 CS2 官匹环境下账号补偿分发的工具平台。在组排过程中，如果出现 VAC 连坐情况，主要责任方需要补偿其他受影响玩家的账号。本网站用于安全、便捷地分发这些补偿账号。

## 功能特性

- 创建可控有效期的账号分发链接
- 账号信息安全存储，链接过期自动失效
- 支持一键复制和下载账号信息
- 完全开源，代码可审计
- 不存储长期数据，保护隐私

## 技术栈

### 前端
- Vue 3
- Vue Router
- Ant Design Vue
- Axios
- Vite

### 后端
- Python 3
- Flask
- SQLite
- Flask-CORS

## 项目结构

```
prime-account-dist/
├── backend/                 # 后端目录
│   ├── app.py              # Flask 应用主文件
│   ├── requirements.txt    # Python 依赖
│   └── README.md           # 后端说明
├── src/                    # 前端源码
│   ├── api/                # API 封装
│   │   └── index.js
│   ├── router/             # 路由配置
│   │   └── index.js
│   ├── utils/              # 工具函数
│   │   └── format.js
│   ├── views/              # 页面组件
│   │   ├── Home.vue        # 首页
│   │   ├── Create.vue      # 创建页面
│   │   └── Link.vue        # 链接访问页面
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── public/                 # 静态资源
├── index.html              # HTML 模板
├── package.json            # 前端依赖
└── vite.config.js          # Vite 配置
```

## 安装与运行

### 前端

1. 安装依赖
```bash
npm install
```

2. 启动开发服务器
```bash
npm run dev
```

3. 构建生产版本
```bash
npm run build
```

### 后端

1. 进入后端目录
```bash
cd backend
```

2. 创建虚拟环境（推荐）
```bash
python -m venv venv
```

3. 激活虚拟环境

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. 安装依赖
```bash
pip install -r requirements.txt
```

5. 启动后端服务
```bash
python app.py
```

后端服务将在 `http://localhost:5000` 启动

## 使用说明

1. 访问首页，点击"创建分发链接"
2. 输入账号列表（格式：账号|密码，每行一个）
3. 选择有效期（1小时到7天）
4. 生成链接并分享给被补偿者
5. 被补偿者通过链接查看、复制或下载账号信息

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

## 安全声明

- 本项目完全开源，所有代码公开可查
- 代码可自行审计，确保无后门
- 不会窃取或保存任何账号数据
- 不进行任何远程上传或隐藏通信
- 数据短期存储，过期自动清理

## 开源协议

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。