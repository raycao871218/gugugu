#!/bin/bash

# 启动FastAPI开发服务器的脚本

echo "正在启动Gugugu FastAPI服务器..."
echo "安装依赖..."

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

echo "启动服务器..."
echo "API服务将在 http://localhost:8000 运行"
echo "API文档在 http://localhost:8000/docs"
echo "按 Ctrl+C 停止服务器"

# 启动服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
