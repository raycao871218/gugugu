# 🚀 Gugugu - Modern FastAPI Application

> 一个现代化的Python Web API项目，基于FastAPI框架构建，集成AI对话功能，采用模块化架构设计。

[![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=flat&logo=python)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg?style=flat&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat)](https://opensource.org/licenses/MIT)

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🏗️ **模块化架构** | 清晰的代码组织，支持快速开发和维护 |
| 🤖 **AI对话集成** | 内置DeepSeek-V3模型，提供智能对话功能 |
| 📊 **完整的CRUD** | 物品管理系统，包含增删改查操作 |
| 📝 **自动文档** | FastAPI自动生成交互式API文档 |
| 🐳 **容器化部署** | 完整的Docker解决方案，一键部署 |
| 🔐 **安全配置** | 环境变量管理，自动密钥生成 |
| 🏥 **健康监控** | 实时API和AI服务状态监控 |
| ⚡ **高性能** | 异步框架，支持高并发访问 |

## 🚀 快速开始

### 🐳 方式一：Docker部署（推荐）

> 💡 **推荐方式**：使用Docker可以避免环境依赖问题，一键部署所有服务。

```bash
# 1. 克隆项目
git clone <repository-url>
cd gugugu

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件，设置您的API密钥和配置

# 3. 自动生成安全密钥（可选）
chmod +x generate-keys.sh
./generate-keys.sh

# 4. 一键启动所有服务
chmod +x docker-start.sh
./docker-start.sh
```

**服务访问地址：**
- 🌐 **API文档**: http://localhost/docs
- 🚀 **API服务**: http://localhost
- 🏥 **健康检查**: http://localhost/health
- 🧪 **流式测试页面**: `stream_example.html` (双击打开)

**快速测试命令：**
```bash
# 测试普通AI接口
curl -X POST "http://localhost/ai/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "你好"}'

# 测试流式AI接口
curl -X POST "http://localhost/ai/chat/stream" \
     -H "Content-Type: application/json" \
     -d '{"message": "请写一首短诗"}' \
     --no-buffer
```

### 💻 方式二：本地开发

```bash
# 1. 安装Python依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 文件配置

# 3. 启动开发服务器
python main.py
```

访问 http://localhost:8000/docs 查看API文档。

## 📁 项目架构

项目采用现代化模块架构设计，代码组织清晰，便于维护和扩展：

```
gugugu/
├── 🚀 main.py                    # 应用入口点 (50行精简代码)
├── 📦 api/                       # API模块目录
│   ├── ⚙️ core/                  # 核心配置和工具
│   │   ├── config.py            # 配置管理和环境变量
│   │   └── database.py          # 数据库连接和模拟
│   ├── 📋 models/               # 数据模型定义
│   │   └── schemas.py           # Pydantic数据模型
│   └── 🛣️ routers/              # 功能路由模块
│       ├── ai.py                # 🤖 AI对话相关端点 (包含流式接口)
│       └── health.py            # 🏥 健康检查端点
├── 🐳 docker-compose.yml        # Docker服务编排
├── 📄 Dockerfile               # Docker镜像构建文件
├── 📋 requirements.txt          # Python依赖清单
├── 🔒 .env.example             # 环境变量模板
├── 📚 docs/                     # 项目文档
│   ├── SECURITY.md             # 🔐 安全配置指南
│   ├── DEPLOYMENT.md           # 🚀 部署检查清单
│   └── RESTRUCTURING.md        # 📝 重构文档说明
├── 🔧 generate-keys.sh          # 安全密钥生成脚本
├── 📖 AI_API_GUIDE.md          # 🤖 AI接口详细使用指南
└── 🧪 stream_example.html       # 流式接口测试页面
```

> 📖 **详细说明**: 查看 [RESTRUCTURING.md](./RESTRUCTURING.md) 了解完整的重构过程和架构设计思路。

## 🔐 安全配置

### ⚡ 快速安全设置

使用自动化脚本一键生成安全配置：

```bash
chmod +x generate-keys.sh
./generate-keys.sh
```

**脚本功能：**
- ✅ 自动生成256位安全SECRET_KEY
- ✅ 创建强随机数据库密码
- ✅ 设置正确的文件权限(600)
- ✅ 提供详细配置指导

### 🔒 手动配置

如果您需要手动配置环境变量：

```bash
# 复制模板文件
cp .env.example .env

# 编辑配置文件
# 必须配置：DEEPSEEK_API_KEY
# 建议配置：SECRET_KEY, DB_PASSWORD
vim .env
```

> 📚 **详细指南**: 查看 [SECURITY.md](./SECURITY.md) 获取完整的安全配置说明和最佳实践。

## 🚀 部署指南

### 生产环境部署检查清单

在生产环境部署前，请确保完成以下检查：

- [ ] 环境变量配置完整
- [ ] 安全密钥已更新
- [ ] SSL证书已配置
- [ ] 防火墙规则已设置
- [ ] 日志监控已启用

> 📋 **完整清单**: 查看 [DEPLOYMENT.md](./DEPLOYMENT.md) 获取详细的部署步骤和检查清单。

## 🛠️ API接口文档

### 📊 基础服务端点

| 方法 | 端点 | 描述 | 状态 |
|------|------|------|------|
| `GET` | `/` | 欢迎消息和系统信息 | ✅ |
| `GET` | `/health` | 系统健康状态检查 | ✅ |

### 🤖 AI功能端点

| 方法 | 端点 | 描述 | 状态 |
|------|------|------|------|
| `GET` | `/ai/health` | AI服务连接状态检查 | ✅ |
| `POST` | `/ai/chat` | 智能对话接口 | ✅ |
| `POST` | `/ai/chat/stream` | 流式智能对话接口 | ✅ |

### 📚 RAG (检索增强生成) 端点

| 方法 | 端点 | 描述 | 状态 |
|------|------|------|------|
| `POST` | `/ai/rag/chat` | 基于文档的智能问答 | ✅ |
| `POST` | `/ai/rag/chat-advanced` | 增强RAG对话 (关键词+语义混合排序) | ✅ |
| `GET` | `/ai/documents` | 获取已处理文档列表 | ✅ |
| `GET` | `/ai/documents/stats` | 获取向量存储统计信息 | ✅ |
| `POST` | `/ai/documents/process` | 处理新文档 | ✅ |
| `POST` | `/ai/documents/process-batch` | 批量处理文档 | ✅ |
| `POST` | `/ai/documents/process-splendor` | 处理璀璨宝石规则文档 | ✅ |
| `DELETE` | `/ai/documents/{file_path}` | 从向量存储中删除文档 | ✅ |
| `POST` | `/ai/rag/search` | 纯文档搜索 (无AI生成) | ✅ |

## 📚 RAG (检索增强生成) 功能

### 🎯 功能概述

RAG功能允许您基于上传的文档进行智能问答，系统会自动检索相关文档内容并结合AI模型生成准确的回答。

### ✨ 主要特性

- **📄 文档处理**: 支持Markdown (.md) 和文本 (.txt) 文件
- **🔍 智能检索**: 使用向量相似度搜索找到最相关的文档片段
- **💬 上下文对话**: 基于检索到的内容生成准确回答
- **📊 来源追踪**: 提供回答的文档来源和相似度信息
- **🎯 精准搜索**: 可指定特定文档或搜索全部文档
- **📝 文件名支持**: 支持使用简洁的文件名而不是完整路径

### 🚀 快速开始

#### 1. 处理璀璨宝石规则文档
```bash
curl -X POST http://localhost:8000/ai/documents/process-splendor
```

#### 2. 查看已处理文档和统计信息
```bash
# 查看文档列表
curl http://localhost:8000/ai/documents

# 查看统计信息
curl http://localhost:8000/ai/documents/stats
```

#### 3. 进行RAG问答
```bash
# 标准模式 - 使用文件名（推荐）
curl -X POST http://localhost:8000/ai/rag/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "璀璨宝石游戏的胜利条件是什么？",
    "file_name": "splendor.md",
    "max_tokens": 500
  }'

# 高级模式 (增强排序) - 使用文件名
curl -X POST http://localhost:8000/ai/rag/chat-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How to win in Splendor?",
    "file_name": "splendor.md",
    "max_tokens": 500,
    "top_k": 5
  }'

# 向后兼容：仍支持完整路径
curl -X POST http://localhost:8000/ai/rag/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "璀璨宝石游戏的胜利条件是什么？",
    "file_path": "/full/path/to/splendor.md",
    "max_tokens": 500
  }'
```

#### 4. 纯文档搜索
```bash
# 使用文件名搜索
curl -X POST "http://localhost:8000/ai/rag/search?query=victory+conditions&file_name=splendor.md&top_k=3&min_similarity=0.7"

# 搜索所有文档
curl -X POST "http://localhost:8000/ai/rag/search?query=victory+conditions&top_k=3&min_similarity=0.7"
```

### 📖 使用示例

#### 处理自定义文档
```bash
# 使用文件名（推荐）
curl -X POST http://localhost:8000/ai/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "file_name": "your_document.md",
    "force_reprocess": false
  }'

# 使用完整路径（向后兼容）
curl -X POST http://localhost:8000/ai/documents/process \
  -H "Content-Type: application/json" \
  -d '{
    "file_path": "/path/to/your/document.md",
    "force_reprocess": false
  }'
```

#### 指定文档进行问答
```bash
# 使用文件名
curl -X POST http://localhost:8000/ai/rag/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "游戏中的宝石种类有哪些？",
    "file_name": "splendor.md",
    "top_k": 3
  }'
```

### 🎮 Web演示界面

访问项目根目录的 `rag_demo.html` 文件，体验可视化的RAG问答界面：

- 📁 选择知识库文档
- 💬 实时对话交互
- 📊 查看文档来源和相似度
- 🎨 美观的用户界面

### 🔧 技术实现

- **向量化**: 使用OpenAI Embedding API生成文档向量
- **存储**: 基于NumPy和JSON的本地向量存储
- **检索**: 余弦相似度计算找到最相关内容
- **生成**: 结合检索内容和AI模型生成回答

### 🚀 RAG系统增强功能

#### 🎯 双模式对话系统
- **标准模式** (`/ai/rag/chat`): 基于语义相似度的快速问答
- **高级模式** (`/ai/rag/chat-advanced`): 增强排序，结合关键词匹配和语义理解

#### 📊 统计与管理
- **统计信息** (`/ai/documents/stats`): 实时查看向量存储状态
- **批量处理** (`/ai/documents/process-batch`): 一次性处理多个文档
- **文档删除** (`DELETE /ai/documents/{file_path}`): 从向量存储中移除文档

#### 🔍 纯搜索功能
- **文档搜索** (`/ai/rag/search`): 无AI生成的纯文档检索
- **相似度过滤**: 支持最小相似度阈值设置
- **多维评分**: 语义相似度 + 关键词匹配的综合评分

#### 📈 增强的评分系统
```
综合得分 = 0.7 × 语义相似度 + 0.3 × 关键词匹配度
```

#### 🌐 增强版演示界面
- **实时统计面板**: 显示文档数量、片段数、存储大小
- **模式切换**: 标准/高级模式一键切换
- **高级参数控制**: 自定义返回结果数、温度参数等
- **详细评分显示**: 显示语义相似度、综合得分、关键词匹配度
- **文件名支持**: 使用简洁的文件名而不是完整路径

#### 📝 文件名功能改进 (NEW!)
- **简化API**: 支持使用文件名（如`splendor.md`）而不是完整路径
- **自动搜索**: 系统自动在`doc/`目录中查找文件
- **向后兼容**: 完全兼容原有的`file_path`参数
- **用户友好**: 演示界面现在使用文件名，更加简洁

---

## 📝 数据模型示例

#### AI对话请求
```json
{
  "message": "你好，请介绍一下你自己",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### RAG对话请求
```json
{
  "message": "璀璨宝石游戏的胜利条件是什么？",
  "file_name": "splendor.md",
  "max_tokens": 1000,
  "temperature": 0.7,
  "top_k": 5
}
```

#### 文档处理请求
```json
{
  "file_name": "splendor.md",
  "force_reprocess": false
}
```

#### AI流式对话请求
```json
{
  "message": "请写一首关于春天的诗",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

#### RAG对话响应
```json
{
  "response": "根据游戏规则，胜利条件是...",
  "model": "deepseek-ai/DeepSeek-V3",
  "sources": [
    {
      "file_path": "/path/to/splendor.md",
      "file_name": "splendor.md",
      "chunk_index": 0,
      "similarity": 0.85,
      "content_preview": "游戏规则摘要..."
    }
  ],
  "usage": {
    "completion_tokens": 150,
    "prompt_tokens": 800,
    "total_tokens": 950
  }
}
```

#### AI对话响应
```json
{
  "response": "你好！我是DeepSeek Chat，一个AI助手...",
  "model": "deepseek-ai/DeepSeek-V3",
  "usage": {
    "completion_tokens": 100,
    "prompt_tokens": 10,
    "total_tokens": 110
  }
}
```

#### AI流式响应 (Server-Sent Events)
```
data: {"type": "start", "model": "deepseek-ai/DeepSeek-V3"}

data: {"type": "content", "content": "春"}

data: {"type": "content", "content": "天"}

data: {"type": "content", "content": "来了"}

data: {"type": "done"}
```

#### 物品数据模型
```json
{
  "id": 1,
  "name": "示例物品",
  "description": "这是一个示例物品",
  "price": 99.99,
  "is_available": true
}
```

> 📖 **交互式文档**: 启动服务后访问 http://localhost/docs 查看完整的API文档和在线测试界面。

## 💻 开发指南

### 🛠️ 环境变量配置

项目使用 `.env` 文件管理环境变量，主要配置包括：

| 变量名 | 描述 | 示例值 | 必需 |
|--------|------|--------|------|
| `DEBUG` | 调试模式开关 | `true`/`false` | ❌ |
| `HOST` | 服务器绑定主机 | `0.0.0.0` | ❌ |
| `PORT` | 服务器监听端口 | `8000` | ❌ |
| `SECRET_KEY` | 应用安全密钥 | `随机256位字符串` | ✅ |
| `DEEPSEEK_API_KEY` | AI服务API密钥 | `sk-xxxxx` | ✅ |
| `DB_PASSWORD` | 数据库连接密码 | `强随机密码` | ✅ |

### ➕ 添加新功能

遵循模块化架构，添加新功能的推荐步骤：

1. **📋 定义数据模型**
   ```bash
   # 在 api/models/schemas.py 中定义Pydantic模型
   ```

2. **🛣️ 创建路由模块**
   ```bash
   # 在 api/routers/ 中创建新的路由文件
   ```

3. **🔌 注册路由**
   ```bash
   # 在 main.py 中注册新的路由模块
   ```

4. **✅ 更新文档**
   ```bash
   # 更新README.md和相关文档
   ```

### 🏗️ 生产环境部署

在生产环境中的最佳实践：

```bash
# 1. 使用生产级ASGI服务器
pip install gunicorn uvicorn[standard]

# 2. 启动生产服务器 (4个工作进程)
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 3. 或使用Docker生产配置
docker-compose -f docker-compose.prod.yml up -d
```

**生产环境检查清单：**
- ✅ 更改默认SECRET_KEY
- ✅ 设置具体的CORS允许域名
- ✅ 配置HTTPS/SSL证书
- ✅ 设置日志记录和监控
- ✅ 配置反向代理(Nginx)
- ✅ 设置环境变量文件权限

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 📝 提交规范

- 🐛 **Bug修复**: `fix: 修复XXX问题`
- ✨ **新功能**: `feat: 添加XXX功能`
- 📚 **文档**: `docs: 更新XXX文档`
- 🔧 **配置**: `config: 更新XXX配置`

## 📄 许可证

本项目采用 [MIT License](https://opensource.org/licenses/MIT) 开源许可证。

---

<div align="center">

**🎉 感谢使用 Gugugu！**

如果这个项目对你有帮助，请考虑给它一个 ⭐️

[报告问题](../../issues) · [功能请求](../../issues) · [贡献代码](../../pulls)

</div>
