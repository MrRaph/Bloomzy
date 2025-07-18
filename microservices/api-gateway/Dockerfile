FROM nginx:alpine

# Install curl for health checks
RUN apk add --no-cache curl

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Create log directory
RUN mkdir -p /var/log/nginx

# Create non-root user
RUN adduser -D -s /bin/sh nginxuser

# Set proper permissions
RUN chown -R nginxuser:nginxuser /var/cache/nginx /var/log/nginx \
    && chmod -R 755 /var/cache/nginx /var/log/nginx

# Create PID directory
RUN mkdir -p /var/run/nginx && chown nginxuser:nginxuser /var/run/nginx

# Switch to non-root user
USER nginxuser

# Expose ports
EXPOSE 80 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"]