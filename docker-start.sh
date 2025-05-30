#!/bin/bash

# Docker启动脚本

echo "🐳 Gugugu FastAPI Docker 部署脚本"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查docker compose是否可用
if ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose未安装或不可用，请确保Docker Desktop已安装"
    exit 1
fi

# 显示选项菜单
echo "请选择操作："
echo "1) 启动服务 (支持热重载的开发环境)"
echo "2) 停止所有服务"
echo "3) 查看服务状态"
echo "4) 查看日志"
echo "5) 重启服务"

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "🚀 启动服务（支持热重载）..."
        docker compose up -d --build
        echo "✅ 服务已启动！"
        echo "📍 API服务: http://localhost:8000"
        echo "📚 API文档: http://localhost:8000/docs"
        echo "🏥 健康检查: http://localhost:8000/health"
        echo "🔄 热重载已启用 - 代码更改将自动生效"
        ;;
    2)
        echo "🛑 停止所有服务..."
        docker compose down
        echo "✅ 所有服务已停止"
        ;;
    3)
        echo "📊 服务状态："
        docker compose ps
        ;;
    4)
        echo "📋 选择要查看的日志："
        echo "1) FastAPI应用日志"
        echo "2) Nginx日志"
        echo "3) Redis日志"
        echo "4) 所有服务日志"
        read -p "请输入选项 (1-4): " log_choice
        
        case $log_choice in
            1)
                docker compose logs -f app
                ;;
            2)
                docker compose logs -f nginx
                ;;
            3)
                docker compose logs -f redis
                ;;
            4)
                docker compose logs -f
                ;;
            *)
                echo "无效选项"
                ;;
        esac
        ;;
    5)
        echo "🔄 重启服务..."
        docker compose restart
        echo "✅ 服务已重启"
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
