# 安全配置指南

## 概述

本文档介绍了Gugugu API项目的安全配置最佳实践。

## 环境变量安全

### 敏感信息管理

项目使用`.env`文件管理敏感配置：
- `OPENAI_API_KEY`: AI服务API密钥
- `POSTGRES_PASSWORD`: 数据库密码  
- `SECRET_KEY`: 应用安全密钥

### 初始化配置

```bash
# 使用密钥生成脚本
./generate-keys.sh

# 手动编辑API密钥
nano .env
```

## 密钥生成

### SECRET_KEY生成
```bash
# 使用Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# 使用openssl
openssl rand -base64 32
```

## 生产环境安全

### 检查清单
- [ ] 所有默认密码已更改
- [ ] DEBUG模式已关闭
- [ ] 使用HTTPS
- [ ] 限制CORS域名
- [ ] 设置防火墙规则

### Docker安全
- 容器以非root用户运行
- 仅暴露必要端口
- 定期更新镜像

## 监控和备份

### 数据库备份
```bash
# 备份
docker exec gugugu-postgres pg_dump -U gugugu_user gugugu > backup.sql

# 恢复  
docker exec -i gugugu-postgres psql -U gugugu_user gugugu < backup.sql
```

## 故障排除

### 环境变量检查
```bash
# 查看容器环境变量
docker exec gugugu-api printenv | grep -E "OPENAI|POSTGRES"

# 测试AI服务
curl http://localhost:8000/ai/health
```

---

**重要**: 定期更新和审查安全配置，确保系统安全。
