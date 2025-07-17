#!/bin/bash

# Script pour démarrer uniquement les services de monitoring
# Usage: ./scripts/start-monitoring.sh

echo "🚀 Démarrage des services de monitoring Bloomzy..."

# Vérifier que les fichiers de configuration existent
if [ ! -f "monitoring/prometheus.yml" ]; then
    echo "❌ Fichier de configuration Prometheus manquant: monitoring/prometheus.yml"
    exit 1
fi

if [ ! -d "monitoring/grafana/provisioning" ]; then
    echo "❌ Répertoire de configuration Grafana manquant: monitoring/grafana/provisioning"
    exit 1
fi

# Démarrer les services de monitoring
docker compose -f docker-compose.monitoring.yml up -d

echo "✅ Services de monitoring démarrés:"
echo "   - Prometheus: http://localhost:9090"
echo "   - Grafana: http://localhost:3001 (admin/admin)"
echo "   - Node Exporter: http://localhost:9100"
echo "   - cAdvisor: http://localhost:8080"

# Attendre que les services soient prêts
echo "⏳ Vérification de l'état des services..."
sleep 10

# Vérifier l'état des services
docker compose -f docker-compose.monitoring.yml ps