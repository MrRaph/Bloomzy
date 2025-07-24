# API Gateway Configuration

## Overview

The API Gateway serves as the single entry point for all client requests to the microservices. It handles request routing, authentication, rate limiting, and cross-cutting concerns.

## Architecture

The API Gateway is implemented using Nginx with the following features:

- **Request Routing**: Route requests to appropriate microservices
- **Load Balancing**: Distribute requests across service instances
- **Authentication**: Validate JWT tokens (delegated to auth service)
- **Rate Limiting**: Prevent abuse and ensure fair usage
- **CORS Handling**: Manage cross-origin requests
- **Health Checks**: Monitor service health
- **Metrics**: Export metrics for monitoring

## Configuration

### Service Upstreams

```nginx
upstream auth-service {
    server auth-service:5001;
    keepalive 32;
}

upstream plants-service {
    server plants-service:5002;
    keepalive 32;
}

upstream notifications-service {
    server notifications-service:5003;
    keepalive 32;
}
```

### Routing Rules

| Path Pattern | Target Service | Description |
|--------------|----------------|-------------|
| `/auth/*` | auth-service | Authentication endpoints |
| `/indoor-plants/*` | plants-service | Plant catalog endpoints |
| `/user-plants/*` | plants-service | User plant collection endpoints |
| `/notifications/*` | notifications-service | Notification endpoints |

### Rate Limiting

```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=auth:10m rate=5r/s;
```

Rate limits:
- API endpoints: 10 requests per second
- Auth endpoints: 5 requests per second
- Burst: 20 requests for API, 10 for auth

### CORS Configuration

```nginx
add_header 'Access-Control-Allow-Origin' 'http://localhost:8080' always;
add_header 'Access-Control-Allow-Credentials' 'true' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'Accept,Authorization,Cache-Control,Content-Type,DNT,If-Modified-Since,Keep-Alive,Origin,User-Agent,X-Requested-With' always;
```

## Health Checks

### Gateway Health

- **Endpoint**: `GET /health`
- **Port**: 8080
- **Response**: `200 OK` with "healthy" message

### Service Health Checks

- **Auth Service**: `GET /health/auth`
- **Plants Service**: `GET /health/plants`
- **Notifications Service**: `GET /health/notifications`

## Monitoring

### Metrics Endpoint

- **Endpoint**: `GET /metrics`
- **Port**: 8080
- **Format**: Nginx stub_status module

### Prometheus Integration

The gateway exposes metrics for:
- Request rates
- Response times
- Error rates
- Upstream health
- Connection statistics

## Security

### Authentication

The gateway validates JWT tokens by:
1. Extracting token from Authorization header
2. Forwarding token to auth service for validation
3. Allowing/denying request based on validation result

### Headers

The gateway adds security headers:
- `X-Request-ID`: Unique request identifier
- `X-Forwarded-For`: Client IP forwarding
- `X-Forwarded-Proto`: Protocol forwarding

## Load Balancing

### Algorithm

- **Default**: Round-robin
- **Failover**: Automatic failover to healthy upstream
- **Keep-alive**: Connection pooling for better performance

### Configuration

```nginx
upstream plants-service {
    server plants-service:5002 weight=1;
    server plants-service-2:5002 weight=1;
    keepalive 32;
}
```

## Logging

### Access Logs

Format includes:
- Client IP
- Request method and URI
- Response status and size
- Response time
- User agent
- Forwarded headers

### Error Logs

- Level: `warn`
- Location: `/var/log/nginx/error.log`

## Deployment

### Docker Configuration

```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80 8080
```

### Environment Variables

- `NGINX_PORT`: Main port (default: 80)
- `NGINX_HEALTH_PORT`: Health check port (default: 8080)

## Testing

### Health Check

```bash
curl -f http://localhost:8001/health
```

### Service Routing

```bash
# Test auth service
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password"}'

# Test plants service
curl http://localhost:8000/indoor-plants

# Test notifications service
curl -H "Authorization: Bearer <token>" http://localhost:8000/notifications
```

## Troubleshooting

### Common Issues

1. **Service Unavailable (503)**
   - Check upstream service health
   - Verify service discovery registration
   - Check network connectivity

2. **CORS Errors**
   - Verify CORS configuration
   - Check allowed origins
   - Ensure preflight handling

3. **Rate Limiting (429)**
   - Check rate limit configuration
   - Verify client IP detection
   - Adjust limits if needed

### Debug Commands

```bash
# Check nginx configuration
nginx -t

# View access logs
tail -f /var/log/nginx/access.log

# View error logs
tail -f /var/log/nginx/error.log

# Check upstream status
curl http://localhost:8080/metrics
```

## Performance Tuning

### Worker Processes

```nginx
worker_processes auto;
worker_connections 1024;
```

### Caching

```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g;
proxy_cache api_cache;
proxy_cache_valid 200 302 10m;
proxy_cache_valid 404 1m;
```

### Compression

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1000;
gzip_comp_level 6;
gzip_types
    text/plain
    text/css
    text/xml
    text/javascript
    application/json
    application/javascript
    application/xml+rss
    application/atom+xml
    image/svg+xml;
```

## SSL/TLS Configuration

For production deployment:

```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /etc/ssl/certs/bloomzy.crt;
    ssl_certificate_key /etc/ssl/private/bloomzy.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

## Kong Alternative

For more advanced features, Kong can be used:

```yaml
services:
  - name: auth-service
    url: http://auth-service:5001
    plugins:
      - name: jwt
      - name: rate-limiting
        config:
          minute: 100
      - name: cors
```

## Future Enhancements

1. **GraphQL Gateway**: Implement GraphQL for flexible queries
2. **Service Mesh**: Integrate with Istio for advanced traffic management
3. **Circuit Breakers**: Add resilience patterns
4. **Request Transformation**: Transform requests/responses
5. **API Versioning**: Support multiple API versions
6. **Analytics**: Detailed API usage analytics