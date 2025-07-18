# Bloomzy Microservices Architecture

## Overview

The Bloomzy project has been successfully migrated from a monolithic architecture to a microservices architecture. This document provides a comprehensive guide to understanding, deploying, and maintaining the microservices-based system.

## Architecture Overview

### Services

1. **Auth Service** (`auth-service:5001`)
   - User authentication and authorization
   - JWT token management
   - User profile management
   - API key management

2. **Plants Service** (`plants-service:5002`)
   - Indoor plant catalog management
   - User plant collection management
   - Growth tracking and watering history
   - Plant care recommendations

3. **Notifications Service** (`notifications-service:5003`)
   - Notification scheduling and delivery
   - User preferences management
   - Multi-channel notifications (push, email, SMS)
   - Analytics and reporting

4. **API Gateway** (`api-gateway:80`)
   - Request routing and load balancing
   - Authentication and authorization
   - Rate limiting and security
   - CORS handling

### Infrastructure Components

1. **Service Discovery** (Consul)
   - Service registration and discovery
   - Health checks and monitoring
   - Configuration management

2. **Message Queue** (Redis)
   - Asynchronous task processing
   - Caching layer
   - Session storage

3. **Databases** (PostgreSQL)
   - Separate databases for each service
   - Data isolation and independence

4. **Monitoring Stack**
   - Prometheus for metrics collection
   - Grafana for visualization
   - Jaeger for distributed tracing

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- 8GB+ RAM recommended
- Ports 8000, 8080, 3000, 9090, 16686, 8500 available

### Deployment

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Bloomzy
   ```

2. **Deploy the entire stack:**
   ```bash
   ./scripts/deploy-microservices.sh deploy
   ```

3. **Check deployment status:**
   ```bash
   ./scripts/deploy-microservices.sh status
   ```

### Access Points

- **Frontend**: http://localhost:8080
- **API Gateway**: http://localhost:8000
- **Consul UI**: http://localhost:8500
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Jaeger**: http://localhost:16686

## Service Details

### Auth Service

**Endpoints:**
- `POST /auth/signup` - User registration
- `POST /auth/login` - User authentication
- `POST /auth/logout` - User logout
- `GET /auth/profile` - Get user profile
- `PUT /auth/profile` - Update user profile
- `POST /auth/refresh` - Refresh JWT token
- `POST /auth/verify` - Verify JWT token (internal)

**Features:**
- JWT-based authentication
- Password hashing with PBKDF2
- Token blacklisting for logout
- User profile management
- API key management

### Plants Service

**Endpoints:**
- `GET /indoor-plants` - List all plants
- `POST /indoor-plants` - Create new plant (admin)
- `GET /indoor-plants/{id}` - Get plant details
- `PUT /indoor-plants/{id}` - Update plant (admin)
- `DELETE /indoor-plants/{id}` - Delete plant (admin)
- `GET /user-plants` - List user's plants
- `POST /user-plants` - Add plant to collection
- `GET /user-plants/{id}` - Get user plant details
- `PUT /user-plants/{id}` - Update user plant
- `DELETE /user-plants/{id}` - Remove plant from collection
- `GET /user-plants/{id}/growth` - Get growth entries
- `POST /user-plants/{id}/growth` - Add growth entry
- `GET /user-plants/{id}/watering` - Get watering history
- `POST /user-plants/{id}/watering` - Record watering

**Features:**
- Plant catalog management
- User plant collections
- Growth tracking
- Watering history
- Care recommendations

### Notifications Service

**Endpoints:**
- `GET /notifications` - List user notifications
- `GET /notifications/{id}` - Get notification details
- `POST /notifications/{id}/mark-opened` - Mark as opened
- `POST /notifications/{id}/mark-acted` - Mark as acted upon
- `POST /notifications/{id}/dismiss` - Dismiss notification
- `POST /notifications/{id}/cancel` - Cancel scheduled notification
- `GET /notifications/preferences` - Get user preferences
- `PUT /notifications/preferences` - Update preferences
- `POST /notifications/schedule` - Schedule notification
- `GET /notifications/analytics` - Get analytics
- `POST /notifications/test` - Send test notification

**Features:**
- Multi-channel notifications (push, email, SMS)
- Scheduling and automation
- User preferences management
- Analytics and reporting
- Template management

## Deployment Options

### Development Environment

```bash
# Start infrastructure services
./scripts/deploy-microservices.sh infrastructure

# Start application services
./scripts/deploy-microservices.sh services

# Start monitoring
./scripts/deploy-microservices.sh monitoring
```

### Production Environment

1. **Environment Variables:**
   Create a `.env` file with production settings:
   ```bash
   # Database URLs
   AUTH_DATABASE_URL=postgresql://user:pass@auth-db:5432/auth
   PLANTS_DATABASE_URL=postgresql://user:pass@plants-db:5432/plants
   NOTIFICATIONS_DATABASE_URL=postgresql://user:pass@notifications-db:5432/notifications
   
   # Redis
   REDIS_HOST=redis
   REDIS_PORT=6379
   
   # Consul
   CONSUL_HOST=consul
   CONSUL_PORT=8500
   
   # Secrets
   SECRET_KEY=your-production-secret-key
   ```

2. **Deploy with production settings:**
   ```bash
   docker-compose -f docker-compose.microservices.yml -f docker-compose.prod.yml up -d
   ```

## Monitoring and Observability

### Metrics

Prometheus collects metrics from all services:
- Request rates and latencies
- Error rates
- Resource utilization
- Business metrics

### Alerting

Alert rules are configured for:
- Service availability
- High error rates
- Resource exhaustion
- Database connectivity

### Distributed Tracing

Jaeger provides distributed tracing for:
- Request flow across services
- Performance bottlenecks
- Error propagation

### Health Checks

All services implement health check endpoints:
- `/health` - Service health status
- `/metrics` - Prometheus metrics
- Consul health checks

## Security

### Authentication

- JWT tokens for API authentication
- Token blacklisting for logout
- Service-to-service authentication

### Authorization

- Role-based access control
- Resource-level permissions
- Admin-only endpoints

### Network Security

- Service isolation with Docker networks
- API Gateway as single entry point
- Rate limiting and DDoS protection

## Scaling

### Horizontal Scaling

Services can be scaled independently:
```bash
docker-compose -f docker-compose.microservices.yml up -d --scale auth-service=3
docker-compose -f docker-compose.microservices.yml up -d --scale plants-service=2
```

### Load Balancing

The API Gateway provides load balancing:
- Round-robin distribution
- Health check-based routing
- Session affinity (if needed)

### Database Scaling

Each service has its own database:
- Read replicas for read-heavy workloads
- Connection pooling
- Query optimization

## Troubleshooting

### Common Issues

1. **Service Discovery Issues:**
   ```bash
   # Check Consul health
   curl http://localhost:8500/v1/health/service/auth-service
   
   # Re-register service
   python microservices/service-discovery/register-service.py register auth-service auth-service-1 auth-service 5001 "http://auth-service:5001/health"
   ```

2. **Database Connection Issues:**
   ```bash
   # Check database health
   docker-compose -f docker-compose.microservices.yml ps
   
   # Check database logs
   docker-compose -f docker-compose.microservices.yml logs auth-db
   ```

3. **API Gateway Issues:**
   ```bash
   # Check gateway health
   curl http://localhost:8001/health
   
   # Check nginx logs
   docker-compose -f docker-compose.microservices.yml logs api-gateway
   ```

### Debugging Commands

```bash
# Show all service logs
./scripts/deploy-microservices.sh logs

# Show service status
./scripts/deploy-microservices.sh status

# Run health checks
./scripts/deploy-microservices.sh health

# Stop all services
./scripts/deploy-microservices.sh stop

# Cleanup
./scripts/deploy-microservices.sh cleanup
```

## Development Guidelines

### Adding New Services

1. Create service directory in `microservices/`
2. Implement health check endpoint
3. Add service to Docker Compose
4. Update API Gateway configuration
5. Add monitoring configuration
6. Update documentation

### Inter-Service Communication

- Use HTTP REST APIs for synchronous communication
- Use message queues for asynchronous communication
- Implement circuit breakers for resilience
- Use service discovery for dynamic addressing

### Database Changes

- Use migrations for schema changes
- Maintain backward compatibility
- Test migrations thoroughly
- Document breaking changes

## Performance Optimization

### Caching

- Redis for session and application caching
- CDN for static assets
- Database query caching

### Database Optimization

- Index optimization
- Query optimization
- Connection pooling
- Read replicas

### API Optimization

- Response compression
- Pagination for large datasets
- API versioning
- Rate limiting

## Backup and Recovery

### Database Backups

Automated backups are configured:
- Daily full backups
- Point-in-time recovery
- Cross-region replication

### Service Recovery

- Health checks for automatic recovery
- Circuit breakers for fault tolerance
- Graceful degradation

## Migration from Monolith

The migration from monolithic to microservices architecture involved:

1. **Service Extraction**: Identified service boundaries based on business capabilities
2. **Data Decomposition**: Separated shared database into service-specific databases
3. **API Gateway Implementation**: Centralized routing and authentication
4. **Service Discovery**: Implemented dynamic service registration
5. **Monitoring**: Enhanced observability with distributed tracing
6. **Testing**: Comprehensive testing of inter-service communication

### Migration Benefits

- **Scalability**: Independent scaling of services
- **Resilience**: Isolated failure domains
- **Development Velocity**: Independent development and deployment
- **Technology Diversity**: Use best tools for each service
- **Team Autonomy**: Clear service ownership

## Future Enhancements

### Planned Features

1. **Service Mesh**: Implement Istio for advanced traffic management
2. **Event Streaming**: Add Apache Kafka for event-driven architecture
3. **GraphQL Gateway**: Implement GraphQL for flexible API queries
4. **Kubernetes**: Migrate to Kubernetes for production orchestration
5. **CI/CD**: Implement automated testing and deployment pipelines

### Performance Improvements

1. **Caching Strategy**: Implement multi-level caching
2. **Database Optimization**: Add read replicas and sharding
3. **API Rate Limiting**: Implement intelligent rate limiting
4. **CDN Integration**: Add CDN for static assets

## Support and Maintenance

### Regular Tasks

- Monitor service health and performance
- Update dependencies and security patches
- Review and optimize database queries
- Analyze logs for issues and improvements
- Update documentation

### Emergency Procedures

- Incident response procedures
- Service rollback procedures
- Database recovery procedures
- Communication protocols

## Conclusion

The microservices architecture provides a robust, scalable, and maintainable foundation for the Bloomzy application. This setup enables independent development, deployment, and scaling of different application components while maintaining high availability and performance.

For additional support or questions, please refer to the specific service documentation or contact the development team.