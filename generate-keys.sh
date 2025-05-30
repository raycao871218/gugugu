#!/bin/bash

# 安全密钥生成脚本
echo "🔐 Gugugu API 密钥生成工具"
echo "================================"

# 检查是否已存在.env文件
if [ -f ".env" ]; then
    echo "⚠️  检测到现有的.env文件"
    read -p "是否要备份现有配置并生成新密钥? (y/N): " backup_choice
    if [ "$backup_choice" = "y" ] || [ "$backup_choice" = "Y" ]; then
        cp .env .env.backup.$(date +%Y%m%d_%H%M%S)
        echo "✅ 已备份现有配置"
    else
        echo "❌ 操作已取消"
        exit 0
    fi
fi

# 复制模板文件
cp .env.example .env
echo "📋 已复制环境变量模板"

# 生成SECRET_KEY
echo "🔑 生成应用密钥..."
if command -v python3 &> /dev/null; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
elif command -v openssl &> /dev/null; then
    SECRET_KEY=$(openssl rand -base64 32)
else
    SECRET_KEY="GuguguSecret$(date +%Y%m%d)Key"
fi

# 生成数据库密码
echo "🔐 生成数据库密码..."
if command -v openssl &> /dev/null; then
    DB_PASSWORD=$(openssl rand -base64 16 | tr -d "=+/" | cut -c1-16)
else
    DB_PASSWORD="GuguguDB$(date +%Y%m%d)!"
fi

# 更新.env文件
sed -i.bak "s/your-secret-key-here-change-in-production/$SECRET_KEY/" .env
sed -i.bak "s/your-secure-password-here/$DB_PASSWORD/" .env
rm .env.bak

echo "✅ 密钥生成完成！"
echo "🔑 应用密钥: $SECRET_KEY"
echo "🔐 数据库密码: $DB_PASSWORD"
echo
echo "⚠️  请记得设置您的OPENAI_API_KEY！"
echo "编辑命令: nano .env"

chmod 600 .env
echo "🔒 已设置.env文件权限"
