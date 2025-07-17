#!/bin/bash

# Script pour démarrer tous les services (app + monitoring + database)
# Usage: ./scripts/start-full-stack.sh

echo "🚀 Démarrage de la stack complète Bloomzy..."

# Vérifier que les fichiers de configuration existent
if [ ! -f "monitoring/prometheus.yml" ]; then
    echo "❌ Fichier de configuration Prometheus manquant: monitoring/prometheus.yml"
    exit 1
fi

# Construire et démarrer tous les services
docker compose -f docker-compose.full.yml up -d --build

echo "✅ Stack complète démarrée:"
echo "   - Frontend: http://localhost:8080"
echo "   - Backend: http://localhost:5080"
echo "   - PostgreSQL: localhost:5432"
echo "   - Redis: localhost:6379"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3001 (admin/admin)"
echo "   - Node Exporter: http://localhost:9100"
echo "   - cAdvisor: http://localhost:8081"

# Attendre que les services soient prêts
echo "⏳ Vérification de l'état des services..."
sleep 15

# Vérifier l'état des services
docker compose -f docker-compose.full.yml ps