# Bloomzy Microservices Makefile

# Default target
.PHONY: help
help:
	@echo "Bloomzy Microservices Management"
	@echo ""
	@echo "Available targets:"
	@echo "  build          - Build all microservices"
	@echo "  deploy         - Deploy full microservices stack"
	@echo "  deploy-infra   - Deploy infrastructure services only"
	@echo "  deploy-apps    - Deploy application services only"
	@echo "  deploy-monitoring - Deploy monitoring services only"
	@echo "  start          - Start all services"
	@echo "  stop           - Stop all services"
	@echo "  restart        - Restart all services"
	@echo "  logs           - Show logs from all services"
	@echo "  status         - Show service status"
	@echo "  health         - Run health checks"
	@echo "  clean          - Clean up containers and images"
	@echo "  test           - Run tests"
	@echo "  scale-auth     - Scale auth service to 3 instances"
	@echo "  scale-plants   - Scale plants service to 2 instances"
	@echo "  scale-notifications - Scale notifications service to 2 instances"
	@echo "  backup         - Backup databases"
	@echo "  restore        - Restore databases"
	@echo "  migrate        - Run database migrations"
	@echo "  shell-auth     - Open shell in auth service"
	@echo "  shell-plants   - Open shell in plants service"
	@echo "  shell-notifications - Open shell in notifications service"

# Docker Compose file
COMPOSE_FILE := docker-compose.microservices.yml
COMPOSE_CMD := docker-compose -f $(COMPOSE_FILE)

# Build all services
.PHONY: build
build:
	@echo "Building all microservices..."
	$(COMPOSE_CMD) build

# Deploy full stack
.PHONY: deploy
deploy:
	@echo "Deploying full microservices stack..."
	../scripts/deploy-microservices.sh deploy

# Deploy infrastructure only
.PHONY: deploy-infra
deploy-infra:
	@echo "Deploying infrastructure services..."
	../scripts/deploy-microservices.sh infrastructure

# Deploy applications only
.PHONY: deploy-apps
deploy-apps:
	@echo "Deploying application services..."
	../scripts/deploy-microservices.sh services

# Deploy monitoring only
.PHONY: deploy-monitoring
deploy-monitoring:
	@echo "Deploying monitoring services..."
	../scripts/deploy-microservices.sh monitoring

# Start all services
.PHONY: start
start:
	@echo "Starting all services..."
	$(COMPOSE_CMD) up -d

# Stop all services
.PHONY: stop
stop:
	@echo "Stopping all services..."
	$(COMPOSE_CMD) down

# Restart all services
.PHONY: restart
restart: stop start

# Show logs
.PHONY: logs
logs:
	@echo "Showing logs from all services..."
	$(COMPOSE_CMD) logs -f

# Show service status
.PHONY: status
status:
	@echo "Service status:"
	$(COMPOSE_CMD) ps

# Run health checks
.PHONY: health
health:
	@echo "Running health checks..."
	../scripts/deploy-microservices.sh health

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up containers and images..."
	$(COMPOSE_CMD) down --rmi all --volumes --remove-orphans
	docker system prune -f

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	$(COMPOSE_CMD) exec auth-service python -m pytest tests/
	$(COMPOSE_CMD) exec plants-service python -m pytest tests/
	$(COMPOSE_CMD) exec notifications-service python -m pytest tests/

# Scale services
.PHONY: scale-auth
scale-auth:
	@echo "Scaling auth service to 3 instances..."
	$(COMPOSE_CMD) up -d --scale auth-service=3

.PHONY: scale-plants
scale-plants:
	@echo "Scaling plants service to 2 instances..."
	$(COMPOSE_CMD) up -d --scale plants-service=2

.PHONY: scale-notifications
scale-notifications:
	@echo "Scaling notifications service to 2 instances..."
	$(COMPOSE_CMD) up -d --scale notifications-service=2

# Database operations
.PHONY: backup
backup:
	@echo "Backing up databases..."
	@mkdir -p ../backups
	$(COMPOSE_CMD) exec auth-db pg_dump -U auth_user auth > ../backups/auth_$(shell date +%Y%m%d_%H%M%S).sql
	$(COMPOSE_CMD) exec plants-db pg_dump -U plants_user plants > ../backups/plants_$(shell date +%Y%m%d_%H%M%S).sql
	$(COMPOSE_CMD) exec notifications-db pg_dump -U notifications_user notifications > ../backups/notifications_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "Backups created in ../backups/"

.PHONY: restore
restore:
	@echo "Restoring databases..."
	@echo "Please specify backup files:"
	@echo "  make restore-auth BACKUP_FILE=../backups/auth_20231201_120000.sql"
	@echo "  make restore-plants BACKUP_FILE=../backups/plants_20231201_120000.sql"
	@echo "  make restore-notifications BACKUP_FILE=../backups/notifications_20231201_120000.sql"

.PHONY: restore-auth
restore-auth:
	@echo "Restoring auth database from $(BACKUP_FILE)..."
	$(COMPOSE_CMD) exec -T auth-db psql -U auth_user auth < $(BACKUP_FILE)

.PHONY: restore-plants
restore-plants:
	@echo "Restoring plants database from $(BACKUP_FILE)..."
	$(COMPOSE_CMD) exec -T plants-db psql -U plants_user plants < $(BACKUP_FILE)

.PHONY: restore-notifications
restore-notifications:
	@echo "Restoring notifications database from $(BACKUP_FILE)..."
	$(COMPOSE_CMD) exec -T notifications-db psql -U notifications_user notifications < $(BACKUP_FILE)

# Database migrations
.PHONY: migrate
migrate:
	@echo "Running database migrations..."
	$(COMPOSE_CMD) exec auth-service flask db upgrade
	$(COMPOSE_CMD) exec plants-service flask db upgrade
	$(COMPOSE_CMD) exec notifications-service flask db upgrade

# Shell access
.PHONY: shell-auth
shell-auth:
	@echo "Opening shell in auth service..."
	$(COMPOSE_CMD) exec auth-service bash

.PHONY: shell-plants
shell-plants:
	@echo "Opening shell in plants service..."
	$(COMPOSE_CMD) exec plants-service bash

.PHONY: shell-notifications
shell-notifications:
	@echo "Opening shell in notifications service..."
	$(COMPOSE_CMD) exec notifications-service bash

# Development helpers
.PHONY: dev-setup
dev-setup:
	@echo "Setting up development environment..."
	@echo "Creating .env file..."
	@cp .env.example .env
	@echo "Building services..."
	$(MAKE) build
	@echo "Starting infrastructure..."
	$(MAKE) deploy-infra
	@echo "Development setup complete!"

.PHONY: dev-start
dev-start:
	@echo "Starting development environment..."
	$(COMPOSE_CMD) up -d auth-db plants-db notifications-db redis consul
	@sleep 10
	$(COMPOSE_CMD) up -d auth-service plants-service notifications-service
	@sleep 20
	$(COMPOSE_CMD) up -d api-gateway frontend

.PHONY: dev-stop
dev-stop:
	@echo "Stopping development environment..."
	$(COMPOSE_CMD) down

# Monitoring helpers
.PHONY: monitor
monitor:
	@echo "Opening monitoring dashboards..."
	@echo "Prometheus: http://localhost:9090"
	@echo "Grafana: http://localhost:3000 (admin/admin)"
	@echo "Jaeger: http://localhost:16686"
	@echo "Consul: http://localhost:8500"

.PHONY: metrics
metrics:
	@echo "Collecting metrics..."
	@echo "=== Auth Service Metrics ==="
	@curl -s http://localhost:8000/auth/metrics || echo "Auth service not available"
	@echo ""
	@echo "=== Plants Service Metrics ==="
	@curl -s http://localhost:8000/plants/metrics || echo "Plants service not available"
	@echo ""
	@echo "=== Notifications Service Metrics ==="
	@curl -s http://localhost:8000/notifications/metrics || echo "Notifications service not available"

# Production helpers
.PHONY: prod-deploy
prod-deploy:
	@echo "Deploying to production..."
	@echo "WARNING: This will deploy to production environment!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		$(COMPOSE_CMD) -f docker-compose.prod.yml up -d; \
	else \
		echo "Deployment cancelled."; \
	fi

.PHONY: prod-stop
prod-stop:
	@echo "Stopping production environment..."
	$(COMPOSE_CMD) -f docker-compose.prod.yml down

# Utility targets
.PHONY: check-deps
check-deps:
	@echo "Checking dependencies..."
	@command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed."; exit 1; }
	@command -v docker-compose >/dev/null 2>&1 || { echo "Docker Compose is required but not installed."; exit 1; }
	@echo "All dependencies are installed."

.PHONY: update-images
update-images:
	@echo "Updating Docker images..."
	$(COMPOSE_CMD) pull

.PHONY: prune
prune:
	@echo "Pruning unused Docker resources..."
	docker system prune -f
	docker volume prune -f
	docker network prune -f

# Security helpers
.PHONY: security-scan
security-scan:
	@echo "Running security scan..."
	@echo "Scanning images for vulnerabilities..."
	@for image in bloomzy-auth-service bloomzy-plants-service bloomzy-notifications-service bloomzy-api-gateway; do \
		echo "Scanning $$image..."; \
		docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
			-v $(PWD):/app \
			-w /app \
			aquasec/trivy:latest image $$image; \
	done

# Load testing
.PHONY: load-test
load-test:
	@echo "Running load tests..."
	@echo "Prerequisites: install artillery (npm install -g artillery)"
	@echo "Running basic load test..."
	artillery run ../tests/load/basic-load-test.yml

# Example targets for CI/CD
.PHONY: ci-build
ci-build:
	@echo "CI: Building services..."
	$(MAKE) build

.PHONY: ci-test
ci-test:
	@echo "CI: Running tests..."
	$(MAKE) test

.PHONY: ci-deploy
ci-deploy:
	@echo "CI: Deploying services..."
	$(MAKE) deploy