# Bloomzy Project Makefile
# Gestion centralisée du projet frontend/backend

.PHONY: help install test lint clean dev build docker-build docker-run setup-dev

# Variables
BACKEND_DIR := backend
FRONTEND_DIR := frontend
BACKEND_PORT := 5001
FRONTEND_PORT := 3000

# Couleurs pour les messages
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
BLUE := \033[0;34m
NC := \033[0m # No Color

help: ## Affiche cette aide
	@echo "$(BLUE)Bloomzy Project - Commandes disponibles:$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# =============================================================================
# INSTALLATION ET CONFIGURATION
# =============================================================================

install: install-backend install-frontend ## Installe toutes les dépendances

install-backend: ## Installe les dépendances backend
	@echo "$(YELLOW)Installation des dépendances backend...$(NC)"
	cd $(BACKEND_DIR) && make venv
	@echo "$(GREEN)✅ Backend installé avec succès$(NC)"

install-frontend: ## Installe les dépendances frontend
	@echo "$(YELLOW)Installation des dépendances frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm install
	@echo "$(GREEN)✅ Frontend installé avec succès$(NC)"

setup-dev: install ## Configuration complète de l'environnement de développement
	@echo "$(BLUE)🚀 Environnement de développement configuré$(NC)"
	@echo "$(BLUE)Utilisez 'make dev' pour lancer l'application$(NC)"

# =============================================================================
# DÉVELOPPEMENT
# =============================================================================

dev: ## Lance l'application en mode développement (backend + frontend)
	@echo "$(BLUE)🚀 Lancement de l'application Bloomzy...$(NC)"
	@echo "$(YELLOW)Backend: http://localhost:$(BACKEND_PORT)$(NC)"
	@echo "$(YELLOW)Frontend: http://localhost:$(FRONTEND_PORT)$(NC)"
	@echo "$(BLUE)Appuyez sur Ctrl+C pour arrêter$(NC)"
	@echo ""
	@$(MAKE) -j2 dev-backend dev-frontend

dev-backend: ## Lance uniquement le backend
	@echo "$(YELLOW)Démarrage du backend sur le port $(BACKEND_PORT)...$(NC)"
	cd $(BACKEND_DIR) && source .venv/bin/activate && python -m flask run --host=0.0.0.0 --port=$(BACKEND_PORT)

dev-frontend: ## Lance uniquement le frontend
	@echo "$(YELLOW)Démarrage du frontend sur le port $(FRONTEND_PORT)...$(NC)"
	cd $(FRONTEND_DIR) && npm run dev

# =============================================================================
# TESTS
# =============================================================================

test: test-backend test-frontend ## Lance tous les tests

test-backend: ## Lance les tests backend
	@echo "$(YELLOW)Exécution des tests backend...$(NC)"
	cd $(BACKEND_DIR) && make test
	@echo "$(GREEN)✅ Tests backend terminés$(NC)"

test-frontend: ## Lance les tests frontend
	@echo "$(YELLOW)Exécution des tests frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm test
	@echo "$(GREEN)✅ Tests frontend terminés$(NC)"

test-watch: ## Lance les tests en mode watch
	@echo "$(BLUE)Mode watch activé - les tests se relancent automatiquement$(NC)"
	@$(MAKE) -j2 test-backend-watch test-frontend-watch

test-backend-watch: ## Lance les tests backend en mode watch
	cd $(BACKEND_DIR) && source .venv/bin/activate && pytest --watch

test-frontend-watch: ## Lance les tests frontend en mode watch
	cd $(FRONTEND_DIR) && npm run test -- --watch

# =============================================================================
# QUALITÉ DU CODE
# =============================================================================

lint: lint-backend lint-frontend ## Lance les linters sur tout le projet

lint-backend: ## Lance le linter backend
	@echo "$(YELLOW)Vérification du code backend...$(NC)"
	cd $(BACKEND_DIR) && source .venv/bin/activate && flake8 . || true
	@echo "$(GREEN)✅ Linting backend terminé$(NC)"

lint-frontend: ## Lance le linter frontend
	@echo "$(YELLOW)Vérification du code frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm run lint
	@echo "$(GREEN)✅ Linting frontend terminé$(NC)"

format: format-backend format-frontend ## Formate le code de tout le projet

format-backend: ## Formate le code backend
	@echo "$(YELLOW)Formatage du code backend...$(NC)"
	cd $(BACKEND_DIR) && source .venv/bin/activate && black . || true
	@echo "$(GREEN)✅ Formatage backend terminé$(NC)"

format-frontend: ## Formate le code frontend
	@echo "$(YELLOW)Formatage du code frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm run format
	@echo "$(GREEN)✅ Formatage frontend terminé$(NC)"

# =============================================================================
# BUILD ET DÉPLOIEMENT
# =============================================================================

build: build-backend build-frontend ## Build l'application complète

build-backend: ## Build le backend
	@echo "$(YELLOW)Build du backend...$(NC)"
	cd $(BACKEND_DIR) && source .venv/bin/activate && python -m pip install --upgrade pip
	@echo "$(GREEN)✅ Backend prêt pour la production$(NC)"

build-frontend: ## Build le frontend
	@echo "$(YELLOW)Build du frontend...$(NC)"
	cd $(FRONTEND_DIR) && npm run build
	@echo "$(GREEN)✅ Frontend buildé avec succès$(NC)"

# =============================================================================
# DOCKER
# =============================================================================

docker-build: ## Build les images Docker
	@echo "$(YELLOW)Build des images Docker...$(NC)"
	docker-compose build
	@echo "$(GREEN)✅ Images Docker créées$(NC)"

docker-run: ## Lance l'application avec Docker
	@echo "$(BLUE)🐳 Lancement de l'application avec Docker...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Application disponible sur http://localhost:$(FRONTEND_PORT)$(NC)"

docker-stop: ## Arrête les conteneurs Docker
	@echo "$(YELLOW)Arrêt des conteneurs Docker...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Conteneurs arrêtés$(NC)"

docker-logs: ## Affiche les logs Docker
	docker-compose logs -f

# =============================================================================
# MAINTENANCE
# =============================================================================

clean: clean-backend clean-frontend ## Nettoie les fichiers temporaires

clean-backend: ## Nettoie le backend
	@echo "$(YELLOW)Nettoyage du backend...$(NC)"
	cd $(BACKEND_DIR) && make clean
	@echo "$(GREEN)✅ Backend nettoyé$(NC)"

clean-frontend: ## Nettoie le frontend
	@echo "$(YELLOW)Nettoyage du frontend...$(NC)"
	cd $(FRONTEND_DIR) && rm -rf node_modules dist .vite
	@echo "$(GREEN)✅ Frontend nettoyé$(NC)"

reset: clean install ## Réinitialise complètement le projet
	@echo "$(GREEN)🔄 Projet réinitialisé$(NC)"

# =============================================================================
# UTILITAIRES
# =============================================================================

status: ## Affiche l'état du projet
	@echo "$(BLUE)📊 État du projet Bloomzy$(NC)"
	@echo ""
	@echo "$(YELLOW)Backend:$(NC)"
	@if [ -d "$(BACKEND_DIR)/.venv" ]; then \
		echo "  ✅ Environnement virtuel Python configuré"; \
	else \
		echo "  ❌ Environnement virtuel Python manquant"; \
	fi
	@echo ""
	@echo "$(YELLOW)Frontend:$(NC)"
	@if [ -d "$(FRONTEND_DIR)/node_modules" ]; then \
		echo "  ✅ Dépendances Node.js installées"; \
	else \
		echo "  ❌ Dépendances Node.js manquantes"; \
	fi
	@echo ""
	@echo "$(BLUE)Pour installer les dépendances: make install$(NC)"
	@echo "$(BLUE)Pour lancer l'application: make dev$(NC)"

logs: ## Affiche les logs de l'application
	@echo "$(BLUE)📋 Logs de l'application$(NC)"
	@echo "$(YELLOW)Pour voir les logs en temps réel, utilisez: make dev$(NC)"

# =============================================================================
# DÉVELOPPEMENT SPÉCIFIQUE
# =============================================================================

migrate: ## Lance les migrations de base de données
	@echo "$(YELLOW)Exécution des migrations...$(NC)"
	cd $(BACKEND_DIR) && source .venv/bin/activate && flask db upgrade
	@echo "$(GREEN)✅ Migrations appliquées$(NC)"

seed: ## Initialise la base de données avec des données de test
	@echo "$(YELLOW)Initialisation des données de test...$(NC)"
	cd $(BACKEND_DIR) && source .venv/bin/activate && python -c "from app.seed import seed_database; seed_database()"
	@echo "$(GREEN)✅ Données de test ajoutées$(NC)"

# =============================================================================
# AIDE RAPIDE
# =============================================================================

quick-start: ## Guide de démarrage rapide
	@echo "$(BLUE)🚀 Guide de démarrage rapide Bloomzy$(NC)"
	@echo ""
	@echo "$(YELLOW)1. Installation:$(NC)"
	@echo "   make install"
	@echo ""
	@echo "$(YELLOW)2. Lancement:$(NC)"
	@echo "   make dev"
	@echo ""
	@echo "$(YELLOW)3. Tests:$(NC)"
	@echo "   make test"
	@echo ""
	@echo "$(YELLOW)4. Aide complète:$(NC)"
	@echo "   make help"
	@echo ""
	@echo "$(GREEN)L'application sera disponible sur:$(NC)"
	@echo "  - Frontend: http://localhost:$(FRONTEND_PORT)"
	@echo "  - Backend API: http://localhost:$(BACKEND_PORT)"