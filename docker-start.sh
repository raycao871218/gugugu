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
echo "请选择部署模式："
echo "1) 简单模式 (仅FastAPI应用)"
echo "2) 完整模式 (FastAPI + Nginx + Redis + PostgreSQL)"
echo "3) 停止所有服务"
echo "4) 查看服务状态"
echo "5) 查看日志"

read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "🚀 启动简单模式..."
        docker compose -f docker-compose.simple.yml up -d --build
        echo "✅ 服务已启动！"
        echo "📍 API服务: http://localhost:8000"
        echo "📚 API文档: http://localhost:8000/docs"
        ;;
    2)
        echo "🚀 启动完整模式..."
        docker compose up -d --build
        echo "✅ 服务已启动！"
        echo "📍 Web服务: http://localhost (Nginx代理)"
        echo "📍 API服务: http://localhost:8000 (直接访问)"
        echo "📚 API文档: http://localhost:8000/docs"
        echo "🗄️  PostgreSQL: localhost:5432"
        echo "🔴 Redis: localhost:6379"
        ;;
    3)
        echo "🛑 停止所有服务..."
        docker compose down
        docker compose -f docker-compose.simple.yml down
        echo "✅ 所有服务已停止"
        ;;
    4)
        echo "📊 服务状态："
        docker compose ps
        echo ""
        echo "简单模式服务状态："
        docker compose -f docker-compose.simple.yml ps
        ;;
    5)
        echo "📋 选择要查看的日志："
        echo "1) FastAPI应用日志"
        echo "2) Nginx日志"
        echo "3) 所有服务日志"
        read -p "请输入选项 (1-3): " log_choice
        
        case $log_choice in
            1)
                docker compose logs -f app
                ;;
            2)
                docker compose logs -f nginx
                ;;
            3)
                docker compose logs -f
                ;;
            *)
                echo "无效选项"
                ;;
        esac
        ;;
    *)
        echo "❌ 无效选项"
        exit 1
        ;;
esac
