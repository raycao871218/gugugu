# Gugugu FastAPI 项目

这是一个使用FastAPI框架构建的现代Python Web API项目。

## 功能特性

- ✨ 基于FastAPI框架，性能优异
- 📝 自动生成API文档
- 🔄 CORS支持
- 📊 数据验证和序列化
- 🏥 健康检查端点
- 🎯 RESTful API设计
- 🐳 Docker容器化支持
- 🚀 多环境部署配置

## 快速开始

### 本地开发

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 运行应用

```bash
python main.py
```

或者使用uvicorn直接运行：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Docker部署 🐳

我们提供了完整的Docker解决方案，支持简单模式和完整生产环境模式。

#### 快速启动

使用我们提供的交互式脚本：

```bash
./docker-start.sh
```

#### 手动Docker命令

**简单模式（仅FastAPI应用）：**
```bash
# 使用简单配置启动
docker compose -f docker-compose.simple.yml up -d --build

# 停止服务
docker compose -f docker-compose.simple.yml down
```

**完整模式（包含Nginx、Redis、PostgreSQL）：**
```bash
# 启动完整服务栈
docker compose up -d --build

# 停止所有服务
docker compose down
```

#### Docker构建和运行

```bash
# 构建镜像
docker build -t gugugu-api .

# 运行容器
docker run -d -p 8000:8000 --name gugugu-container gugugu-api
```

#### 服务访问地址

- **API服务**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **Web服务** (完整模式): http://localhost (Nginx代理)

更多Docker相关信息请查看 [DOCKER.md](./DOCKER.md)

## API端点

### 基础端点
- `GET /` - 欢迎消息
- `GET /health` - 健康检查

### 物品管理
- `GET /items` - 获取所有物品
- `GET /items/{item_id}` - 根据ID获取物品
- `POST /items` - 创建新物品
- `PUT /items/{item_id}` - 更新物品
- `DELETE /items/{item_id}` - 删除物品

## 数据模型

### Item
```json
{
  "id": 1,
  "name": "示例物品",
  "description": "这是一个示例物品",
  "price": 99.99,
  "is_available": true
}
```

## 项目结构

```
gugugu/
├── main.py              # 主应用文件
├── requirements.txt     # Python依赖
├── .env                # 环境变量配置
└── README.md           # 项目说明
```

## 开发

### 环境变量

项目使用 `.env` 文件管理环境变量，主要配置包括：

- `DEBUG`: 调试模式
- `HOST`: 服务器主机
- `PORT`: 服务器端口
- `SECRET_KEY`: 安全密钥

### 添加新功能

1. 在 `main.py` 中定义新的数据模型
2. 创建相应的API端点
3. 更新API文档

## 生产部署

在生产环境中，建议：

1. 更改 `.env` 中的 `SECRET_KEY`
2. 设置具体的CORS允许域名
3. 使用生产级的ASGI服务器，如Gunicorn + Uvicorn

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 许可证

MIT License
