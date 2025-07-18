# Bloomzy Microservices Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Bloomzy microservices architecture in different environments.

## Prerequisites

### System Requirements

- **CPU**: 4+ cores recommended
- **Memory**: 8GB+ RAM
- **Storage**: 20GB+ available disk space
- **Network**: Internet connection for image downloads

### Software Requirements

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git
- curl (for health checks)

### Port Requirements

The following ports must be available:

| Service | Port | Description |
|---------|------|-------------|
| Frontend | 8080 | Vue.js frontend |
| API Gateway | 8000 | Main API endpoint |
| API Gateway Health | 8001 | Health checks |
| Grafana | 3000 | Monitoring dashboard |
| Consul | 8500 | Service discovery |
| Prometheus | 9090 | Metrics collection |
| Jaeger | 16686 | Distributed tracing |

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-org/bloomzy.git
cd bloomzy
```

### 2. Deploy Full Stack

```bash
# Make deployment script executable
chmod +x scripts/deploy-microservices.sh

# Deploy everything
./scripts/deploy-microservices.sh deploy
```

### 3. Verify Deployment

```bash
# Check service status
./scripts/deploy-microservices.sh status

# Run health checks
./scripts/deploy-microservices.sh health
```

### 4. Access Applications

- **Frontend**: http://localhost:8080
- **API Gateway**: http://localhost:8000
- **Grafana**: http://localhost:3000 (admin/admin)
- **Consul**: http://localhost:8500

## Detailed Deployment Steps

### Step 1: Infrastructure Services

Deploy supporting services first:

```bash
# Deploy databases, Redis, and Consul
./scripts/deploy-microservices.sh infrastructure

# Wait for services to be ready
sleep 30

# Check infrastructure health
docker-compose -f docker-compose.microservices.yml ps
```

### Step 2: Application Services

Deploy the microservices:

```bash
# Deploy auth, plants, and notifications services
./scripts/deploy-microservices.sh services

# Wait for services to initialize
sleep 60

# Check service health
curl http://localhost:8000/health/auth
curl http://localhost:8000/health/plants
curl http://localhost:8000/health/notifications
```

### Step 3: API Gateway and Frontend

Deploy the gateway and frontend:

```bash
# Deploy API Gateway
docker-compose -f docker-compose.microservices.yml up -d api-gateway

# Deploy Frontend
docker-compose -f docker-compose.microservices.yml up -d frontend
```

### Step 4: Monitoring Stack

Deploy monitoring services:

```bash
# Deploy Prometheus, Grafana, and Jaeger
./scripts/deploy-microservices.sh monitoring

# Access monitoring dashboards
echo "Prometheus: http://localhost:9090"
echo "Grafana: http://localhost:3000"
echo "Jaeger: http://localhost:16686"
```

## Environment Configuration

### Development Environment

Create a `.env.development` file:

```bash
# Database Configuration
AUTH_DATABASE_URL=postgresql://auth_user:auth_password@auth-db:5432/auth
PLANTS_DATABASE_URL=postgresql://plants_user:plants_password@plants-db:5432/plants
NOTIFICATIONS_DATABASE_URL=postgresql://notifications_user:notifications_password@notifications-db:5432/notifications

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Service Discovery
CONSUL_HOST=consul
CONSUL_PORT=8500

# Application Configuration
SECRET_KEY=development-secret-key
FLASK_ENV=development
FLASK_DEBUG=1

# API URLs
VITE_API_URL=http://localhost:8000
```

### Production Environment

Create a `.env.production` file:

```bash
# Database Configuration (use strong passwords)
AUTH_DATABASE_URL=postgresql://auth_user:secure_password@auth-db:5432/auth
PLANTS_DATABASE_URL=postgresql://plants_user:secure_password@plants-db:5432/plants
NOTIFICATIONS_DATABASE_URL=postgresql://notifications_user:secure_password@notifications-db:5432/notifications

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379

# Service Discovery
CONSUL_HOST=consul
CONSUL_PORT=8500

# Application Configuration
SECRET_KEY=super-secure-secret-key-change-this
FLASK_ENV=production
FLASK_DEBUG=0

# API URLs
VITE_API_URL=https://api.bloomzy.com
```

## Service-Specific Configuration

### Auth Service

Environment variables:

```bash
# Database
DATABASE_URL=postgresql://auth_user:password@auth-db:5432/auth

# Security
SECRET_KEY=your-secret-key
JWT_EXPIRATION_HOURS=24

# Service Discovery
CONSUL_HOST=consul
CONSUL_PORT=8500
```

### Plants Service

Environment variables:

```bash
# Database
DATABASE_URL=postgresql://plants_user:password@plants-db:5432/plants

# Dependencies
AUTH_SERVICE_URL=http://auth-service:5001

# Service Discovery
CONSUL_HOST=consul
CONSUL_PORT=8500
```

### Notifications Service

Environment variables:

```bash
# Database
DATABASE_URL=postgresql://notifications_user:password@notifications-db:5432/notifications

# Dependencies
AUTH_SERVICE_URL=http://auth-service:5001
PLANTS_SERVICE_URL=http://plants-service:5002

# Celery Configuration
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Service Discovery
CONSUL_HOST=consul
CONSUL_PORT=8500
```

## Scaling Services

### Horizontal Scaling

Scale services based on load:

```bash
# Scale auth service to 3 instances
docker-compose -f docker-compose.microservices.yml up -d --scale auth-service=3

# Scale plants service to 2 instances
docker-compose -f docker-compose.microservices.yml up -d --scale plants-service=2

# Scale notifications service to 2 instances
docker-compose -f docker-compose.microservices.yml up -d --scale notifications-service=2
```

### Load Balancing

The API Gateway automatically load balances between instances:

```nginx
upstream auth-service {
    server auth-service:5001;
    server auth-service-2:5001;
    server auth-service-3:5001;
}
```

## Health Checks and Monitoring

### Health Check Endpoints

All services expose health check endpoints:

```bash
# Gateway health
curl http://localhost:8001/health

# Service health (through gateway)
curl http://localhost:8000/health/auth
curl http://localhost:8000/health/plants
curl http://localhost:8000/health/notifications

# Direct service health
curl http://auth-service:5001/health
curl http://plants-service:5002/health
curl http://notifications-service:5003/health
```

### Monitoring Setup

Access monitoring dashboards:

```bash
# Prometheus metrics
open http://localhost:9090

# Grafana dashboards
open http://localhost:3000
# Login: admin/admin

# Jaeger tracing
open http://localhost:16686

# Consul service discovery
open http://localhost:8500
```

## Database Management

### Initial Setup

Databases are automatically created with the following schemas:

- **auth**: Users, API keys, sessions
- **plants**: Plant catalog, user plants, growth tracking
- **notifications**: Notifications, preferences, templates

### Migrations

Run database migrations:

```bash
# Auth service migrations
docker-compose -f docker-compose.microservices.yml exec auth-service flask db upgrade

# Plants service migrations
docker-compose -f docker-compose.microservices.yml exec plants-service flask db upgrade

# Notifications service migrations
docker-compose -f docker-compose.microservices.yml exec notifications-service flask db upgrade
```

### Backup and Restore

Backup databases:

```bash
# Auth database backup
docker-compose -f docker-compose.microservices.yml exec auth-db pg_dump -U auth_user auth > auth_backup.sql

# Plants database backup
docker-compose -f docker-compose.microservices.yml exec plants-db pg_dump -U plants_user plants > plants_backup.sql

# Notifications database backup
docker-compose -f docker-compose.microservices.yml exec notifications-db pg_dump -U notifications_user notifications > notifications_backup.sql
```

Restore databases:

```bash
# Auth database restore
docker-compose -f docker-compose.microservices.yml exec -T auth-db psql -U auth_user auth < auth_backup.sql

# Plants database restore
docker-compose -f docker-compose.microservices.yml exec -T plants-db psql -U plants_user plants < plants_backup.sql

# Notifications database restore
docker-compose -f docker-compose.microservices.yml exec -T notifications-db psql -U notifications_user notifications < notifications_backup.sql
```

## Troubleshooting

### Common Issues

1. **Services Not Starting**
   ```bash
   # Check service logs
   docker-compose -f docker-compose.microservices.yml logs auth-service
   docker-compose -f docker-compose.microservices.yml logs plants-service
   docker-compose -f docker-compose.microservices.yml logs notifications-service
   ```

2. **Database Connection Issues**
   ```bash
   # Check database status
   docker-compose -f docker-compose.microservices.yml ps
   
   # Check database logs
   docker-compose -f docker-compose.microservices.yml logs auth-db
   ```

3. **Service Discovery Issues**
   ```bash
   # Check Consul status
   curl http://localhost:8500/v1/health/service/auth-service
   
   # Re-register service
   python microservices/service-discovery/register-service.py register auth-service auth-service-1 auth-service 5001 "http://auth-service:5001/health"
   ```

### Debug Commands

```bash
# View all logs
./scripts/deploy-microservices.sh logs

# Check service status
./scripts/deploy-microservices.sh status

# Run health checks
./scripts/deploy-microservices.sh health

# Enter service container
docker-compose -f docker-compose.microservices.yml exec auth-service bash
```

## Performance Optimization

### Resource Limits

Set resource limits for containers:

```yaml
services:
  auth-service:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

### Caching Configuration

Configure Redis caching:

```bash
# Redis memory configuration
redis-cli CONFIG SET maxmemory 256mb
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

### Database Optimization

Optimize PostgreSQL settings:

```bash
# Increase shared buffers
ALTER SYSTEM SET shared_buffers = '256MB';

# Increase work memory
ALTER SYSTEM SET work_mem = '4MB';

# Reload configuration
SELECT pg_reload_conf();
```

## Security Considerations

### Network Security

- Use Docker networks for service isolation
- Implement proper firewall rules
- Use SSL/TLS for external communication

### Authentication Security

- Use strong JWT secrets
- Implement token rotation
- Use proper password hashing

### Database Security

- Use strong database passwords
- Implement database encryption
- Regular security updates

## Maintenance

### Regular Tasks

1. **Monitor Service Health**
   ```bash
   # Daily health checks
   ./scripts/deploy-microservices.sh health
   ```

2. **Update Dependencies**
   ```bash
   # Update Docker images
   docker-compose -f docker-compose.microservices.yml pull
   ```

3. **Database Maintenance**
   ```bash
   # Vacuum databases
   docker-compose -f docker-compose.microservices.yml exec auth-db psql -U auth_user -c "VACUUM ANALYZE;"
   ```

4. **Log Rotation**
   ```bash
   # Rotate logs
   docker-compose -f docker-compose.microservices.yml exec api-gateway logrotate /etc/logrotate.conf
   ```

### Backup Strategy

- Daily automated backups
- Weekly full system backups
- Monthly backup testing
- Offsite backup storage

## Upgrade Procedures

### Rolling Updates

1. **Update service images**
2. **Deploy one service at a time**
3. **Verify health checks**
4. **Monitor for issues**
5. **Rollback if necessary**

### Database Migrations

1. **Backup databases**
2. **Run migrations in test environment**
3. **Run migrations in production**
4. **Verify data integrity**

## Support and Troubleshooting

### Getting Help

- Check service logs for errors
- Review health check endpoints
- Consult monitoring dashboards
- Review this documentation

### Emergency Procedures

1. **Service Outage**
   - Check service health
   - Review logs
   - Restart affected services
   - Scale up if needed

2. **Database Issues**
   - Check database health
   - Review connection limits
   - Restart database if needed
   - Restore from backup if necessary

3. **Performance Issues**
   - Check resource utilization
   - Review service metrics
   - Scale services if needed
   - Optimize queries if needed