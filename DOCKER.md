# Docker Setup and Usage Guide for Gugugu API

## Overview
This document describes how to build, run, and deploy the Gugugu FastAPI application using Docker.

## Quick Start

### Using Docker Compose (Recommended)
```bash
# Start the application
docker compose up -d app

# Stop the application  
docker compose down

# View logs
docker compose logs app

# Rebuild and restart
docker compose up -d --build app
```

### Using Docker directly
```bash
# Build the image
docker build -t gugugu-api .

# Run the container
docker run -d -p 8000:8000 --name gugugu-container gugugu-api

# Stop and remove container
docker stop gugugu-container && docker rm gugugu-container
```

## Available Services

### Main Application (`app`)
- **Port**: 8000
- **Health Check**: `http://localhost:8000/health`
- **API Documentation**: `http://localhost:8000/docs`
- **Container Name**: `gugugu-api`

### Optional Services (configured but not started by default)
- **Nginx Reverse Proxy**: Port 80/443
- **Redis Cache**: Port 6379  
- **PostgreSQL Database**: Port 5432

## Testing the Application

### Health Check
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### Root Endpoint
```bash
curl http://localhost:8000/
# Expected: {"message":"欢迎使用Gugugu API!"}
```

### API Documentation
Open in browser: `http://localhost:8000/docs`

## Development Workflow

### Development Mode
For development with live code reloading:
```bash
# Mount source code and start with auto-reload
docker compose up -d app
# Note: Volume mounting is configured in docker-compose.yml
```

### Production Mode
For production deployment:
```bash
# Use the built image without volume mounting
docker run -d -p 8000:8000 gugugu-api
```

## Docker Configuration Files

### Dockerfile
- Base image: `python:3.11-slim`
- Installs system dependencies and Python packages
- Creates non-root user for security
- Includes health check configuration
- Exposes port 8000

### docker-compose.yml
- Defines multiple services for complete application stack
- Includes health checks and restart policies
- Configures networking between services
- Sets up persistent volumes for data storage

### .dockerignore
Excludes unnecessary files from Docker build context:
- Git files and directories
- Python cache files
- Development tools and configs
- Documentation files

## Container Management

### Viewing Logs
```bash
# Docker Compose
docker compose logs app
docker compose logs -f app  # Follow logs

# Docker
docker logs gugugu-container
docker logs -f gugugu-container  # Follow logs
```

### Container Shell Access
```bash
# Docker Compose
docker compose exec app /bin/bash

# Docker
docker exec -it gugugu-container /bin/bash
```

### Resource Monitoring
```bash
# View container stats
docker stats gugugu-api

# View container processes
docker compose top app
```

## Troubleshooting

### Container Won't Start
1. Check logs: `docker compose logs app`
2. Verify port availability: `lsof -i :8000`
3. Check Docker daemon: `docker info`

### Health Check Failing
1. Verify application is responding: `curl http://localhost:8000/health`
2. Check container logs for errors
3. Ensure all dependencies are installed

### Build Issues
1. Clear Docker cache: `docker system prune`
2. Rebuild without cache: `docker compose build --no-cache app`
3. Check Dockerfile syntax and requirements.txt

## Security Considerations

- Application runs as non-root user (`user`)
- Only necessary ports are exposed
- Base image is regularly updated (python:3.11-slim)
- Build context excludes sensitive files via .dockerignore

## Performance Optimization

- Multi-stage build process (can be enhanced further)
- Minimal base image (slim variant)
- Dependency caching in Docker layers
- Health checks for container orchestration

## Deployment Options

### Single Container
Suitable for development and small deployments:
```bash
docker run -d -p 8000:8000 gugugu-api
```

### With Reverse Proxy
For production with load balancing:
```bash
docker compose up -d app nginx
```

### Full Stack
With database and cache:
```bash
docker compose up -d
```

## Environment Variables

Available environment variables (set in docker-compose.yml):
- `DEBUG`: Enable debug mode (default: True)
- `HOST`: Host to bind to (default: 0.0.0.0)
- `PORT`: Port to bind to (default: 8000)
- `PROJECT_NAME`: API project name (default: Gugugu API)

## Next Steps

1. **Production Deployment**: Consider using Docker Swarm or Kubernetes
2. **CI/CD Integration**: Automate building and deployment
3. **Monitoring**: Add application monitoring and alerting
4. **Security Scanning**: Implement container vulnerability scanning
5. **Backup Strategy**: Set up automated backups for persistent data
