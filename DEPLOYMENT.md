# 部署检查清单

## 部署前检查

### 1. 环境配置
- [ ] 已配置`.env`文件
- [ ] 已设置强密码和密钥
- [ ] OPENAI_API_KEY已配置
- [ ] DEBUG模式设置正确

### 2. 安全检查
- [ ] `.env`文件权限设置为600
- [ ] 所有默认密码已更改
- [ ] API密钥来自正确环境

### 3. Docker配置  
- [ ] Docker和Docker Compose已安装
- [ ] 容器配置正确
- [ ] 健康检查配置

## 部署步骤

### 1. 初始化配置
```bash
# 克隆项目
git clone <repository-url>
cd gugugu

# 生成安全密钥
./generate-keys.sh

# 编辑API密钥
nano .env
```

### 2. 启动服务
```bash
# 构建并启动
docker compose up -d --build

# 或使用脚本
./docker-start.sh
```

### 3. 验证部署
```bash
# 检查容器状态
docker compose ps

# 测试API
curl http://localhost:8000/health
curl http://localhost:8000/ai/health

# 访问文档
open http://localhost:8000/docs
```

## 部署后检查

### 1. 功能测试
- [ ] API健康检查正常
- [ ] AI服务连接正常  
- [ ] 数据库连接正常
- [ ] Nginx代理正常

### 2. 性能测试
- [ ] API响应时间正常
- [ ] 内存使用合理
- [ ] CPU使用正常

## 生产环境

### SSL/TLS配置
- [ ] SSL证书已安装
- [ ] HTTPS重定向配置
- [ ] 安全头部配置

### 监控和日志
- [ ] 应用监控配置
- [ ] 错误日志收集
- [ ] 性能指标监控

### 备份策略
- [ ] 数据库备份策略
- [ ] 配置文件备份
- [ ] 恢复流程测试

## 常见问题

### 容器无法启动
```bash
# 查看日志
docker compose logs app
```

### AI服务连接失败
```bash
# 测试连接
curl http://localhost:8000/ai/health
```

### 数据库连接问题
```bash
# 检查数据库
docker compose logs postgres
```

## 维护建议

### 定期更新
- [ ] 定期更新Docker镜像
- [ ] 更新Python依赖
- [ ] 安全补丁更新

### 监控检查  
- [ ] 定期检查日志
- [ ] 监控资源使用
- [ ] 性能分析

---

**完成检查清单后，您的API就可以安全运行了！** 🎉
