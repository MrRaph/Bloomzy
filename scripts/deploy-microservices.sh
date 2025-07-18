#!/bin/bash

# Bloomzy Microservices Deployment Script
# This script deploys the entire microservices stack

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker and Docker Compose are installed
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_status "Prerequisites check passed!"
}

# Build all microservices
build_services() {
    print_status "Building microservices..."
    
    # Build auth service
    print_status "Building auth service..."
    docker build -t bloomzy-auth-service:latest ./microservices/auth-service/
    
    # Build plants service
    print_status "Building plants service..."
    docker build -t bloomzy-plants-service:latest ./microservices/plants-service/
    
    # Build notifications service
    print_status "Building notifications service..."
    docker build -t bloomzy-notifications-service:latest ./microservices/notifications-service/
    
    # Build API gateway
    print_status "Building API gateway..."
    docker build -t bloomzy-api-gateway:latest ./microservices/api-gateway/
    
    # Build frontend
    print_status "Building frontend..."
    docker build -t bloomzy-frontend:microservices --build-arg VITE_API_URL=http://localhost:8000 ./frontend/
    
    print_status "All services built successfully!"
}

# Deploy infrastructure services
deploy_infrastructure() {
    print_status "Deploying infrastructure services..."
    
    # Start databases and supporting services
    docker-compose -f docker-compose.microservices.yml up -d \
        auth-db \
        plants-db \
        notifications-db \
        redis \
        consul
    
    print_status "Waiting for infrastructure services to be ready..."
    sleep 30
    
    # Check if services are healthy
    print_status "Checking infrastructure health..."
    docker-compose -f docker-compose.microservices.yml ps
    
    print_status "Infrastructure services deployed!"
}

# Deploy application services
deploy_services() {
    print_status "Deploying application services..."
    
    # Start microservices
    docker-compose -f docker-compose.microservices.yml up -d \
        auth-service \
        plants-service \
        notifications-service \
        celery-worker \
        celery-beat
    
    print_status "Waiting for application services to be ready..."
    sleep 60
    
    # Check if services are healthy
    print_status "Checking application services health..."
    docker-compose -f docker-compose.microservices.yml ps
    
    print_status "Application services deployed!"
}

# Deploy API Gateway and Frontend
deploy_gateway_frontend() {
    print_status "Deploying API Gateway and Frontend..."
    
    # Start API Gateway
    docker-compose -f docker-compose.microservices.yml up -d api-gateway
    
    print_status "Waiting for API Gateway to be ready..."
    sleep 30
    
    # Start Frontend
    docker-compose -f docker-compose.microservices.yml up -d frontend
    
    print_status "Waiting for Frontend to be ready..."
    sleep 30
    
    print_status "API Gateway and Frontend deployed!"
}

# Deploy monitoring services
deploy_monitoring() {
    print_status "Deploying monitoring services..."
    
    # Start monitoring services
    docker-compose -f docker-compose.microservices.yml up -d \
        prometheus \
        grafana \
        jaeger
    
    print_status "Waiting for monitoring services to be ready..."
    sleep 30
    
    print_status "Monitoring services deployed!"
}

# Run health checks
health_checks() {
    print_status "Running health checks..."
    
    # Check auth service
    if curl -f http://localhost:8000/auth/health > /dev/null 2>&1; then
        print_status "Auth service is healthy"
    else
        print_warning "Auth service health check failed"
    fi
    
    # Check plants service
    if curl -f http://localhost:8000/indoor-plants > /dev/null 2>&1; then
        print_status "Plants service is healthy"
    else
        print_warning "Plants service health check failed"
    fi
    
    # Check notifications service
    if curl -f http://localhost:8000/notifications > /dev/null 2>&1; then
        print_status "Notifications service is healthy"
    else
        print_warning "Notifications service health check failed"
    fi
    
    # Check API Gateway
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        print_status "API Gateway is healthy"
    else
        print_warning "API Gateway health check failed"
    fi
    
    # Check Frontend
    if curl -f http://localhost:8080 > /dev/null 2>&1; then
        print_status "Frontend is healthy"
    else
        print_warning "Frontend health check failed"
    fi
    
    print_status "Health checks completed!"
}

# Show deployment summary
show_summary() {
    print_status "Deployment Summary:"
    echo ""
    echo "🌐 Frontend: http://localhost:8080"
    echo "🚪 API Gateway: http://localhost:8000"
    echo "🔐 Auth Service: http://localhost:8000/auth"
    echo "🌱 Plants Service: http://localhost:8000/indoor-plants"
    echo "📱 Notifications Service: http://localhost:8000/notifications"
    echo ""
    echo "🎯 Monitoring:"
    echo "  📊 Prometheus: http://localhost:9090"
    echo "  📈 Grafana: http://localhost:3000 (admin/admin)"
    echo "  🔍 Jaeger: http://localhost:16686"
    echo "  🏥 Consul: http://localhost:8500"
    echo ""
    echo "📋 Service Status:"
    docker-compose -f docker-compose.microservices.yml ps
}

# Cleanup function
cleanup() {
    print_status "Cleaning up old containers and images..."
    
    # Stop and remove containers
    docker-compose -f docker-compose.microservices.yml down --remove-orphans
    
    # Remove unused images
    docker image prune -f
    
    print_status "Cleanup completed!"
}

# Main deployment function
main() {
    print_status "Starting Bloomzy Microservices Deployment..."
    
    case "${1:-deploy}" in
        "build")
            check_prerequisites
            build_services
            ;;
        "deploy")
            check_prerequisites
            build_services
            deploy_infrastructure
            deploy_services
            deploy_gateway_frontend
            deploy_monitoring
            health_checks
            show_summary
            ;;
        "infrastructure")
            check_prerequisites
            deploy_infrastructure
            ;;
        "services")
            check_prerequisites
            deploy_services
            ;;
        "monitoring")
            check_prerequisites
            deploy_monitoring
            ;;
        "health")
            health_checks
            ;;
        "cleanup")
            cleanup
            ;;
        "stop")
            print_status "Stopping all services..."
            docker-compose -f docker-compose.microservices.yml down
            print_status "All services stopped!"
            ;;
        "logs")
            docker-compose -f docker-compose.microservices.yml logs -f
            ;;
        "status")
            docker-compose -f docker-compose.microservices.yml ps
            ;;
        *)
            echo "Usage: $0 {build|deploy|infrastructure|services|monitoring|health|cleanup|stop|logs|status}"
            echo ""
            echo "Commands:"
            echo "  build         - Build all microservices"
            echo "  deploy        - Full deployment (default)"
            echo "  infrastructure - Deploy databases and supporting services"
            echo "  services      - Deploy application services"
            echo "  monitoring    - Deploy monitoring services"
            echo "  health        - Run health checks"
            echo "  cleanup       - Clean up old containers and images"
            echo "  stop          - Stop all services"
            echo "  logs          - Show logs from all services"
            echo "  status        - Show status of all services"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"