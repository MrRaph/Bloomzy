#!/bin/bash

# Script de restauration pour Bloomzy
# Usage: ./scripts/restore.sh <backup_name>

if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_name>"
    echo "Exemple: $0 bloomzy_backup_20240117_143022"
    exit 1
fi

BACKUP_NAME=$1
BACKUP_DIR="backups"

echo "🔄 Démarrage de la restauration Bloomzy..."
echo "📦 Backup à restaurer: $BACKUP_NAME"

# Vérifier que les fichiers de backup existent
if [ ! -f "$BACKUP_DIR/${BACKUP_NAME}_manifest.txt" ]; then
    echo "❌ Backup non trouvé: $BACKUP_NAME"
    echo "Backups disponibles:"
    ls -1 "$BACKUP_DIR/"*_manifest.txt 2>/dev/null | sed 's/.*\///g' | sed 's/_manifest\.txt//g' || echo "Aucun backup disponible"
    exit 1
fi

# Afficher le manifest
echo "📋 Manifest du backup:"
cat "$BACKUP_DIR/${BACKUP_NAME}_manifest.txt"
echo

# Demander confirmation
read -p "Voulez-vous continuer avec la restauration? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Restauration annulée"
    exit 1
fi

# Arrêter les services
echo "🛑 Arrêt des services..."
docker compose -f docker-compose.full.yml down

# Fonction pour restaurer PostgreSQL
restore_postgres() {
    echo "🔄 Restauration de PostgreSQL..."
    
    if [ -f "$BACKUP_DIR/${BACKUP_NAME}_postgres.sql" ]; then
        # Démarrer seulement PostgreSQL
        docker compose -f docker-compose.full.yml up -d postgres
        sleep 10
        
        # Restaurer la base de données
        docker exec -i bloomzy-postgres psql -U bloomzy -d bloomzy < "$BACKUP_DIR/${BACKUP_NAME}_postgres.sql"
        
        echo "✅ Restauration PostgreSQL terminée"
    else
        echo "⚠️  Fichier de sauvegarde PostgreSQL non trouvé"
    fi
}

# Fonction pour restaurer Redis
restore_redis() {
    echo "🔄 Restauration de Redis..."
    
    if [ -f "$BACKUP_DIR/${BACKUP_NAME}_redis.rdb" ]; then
        # Démarrer seulement Redis
        docker compose -f docker-compose.full.yml up -d redis
        sleep 5
        
        # Arrêter Redis pour copier le fichier
        docker compose -f docker-compose.full.yml stop redis
        
        # Copier le fichier de sauvegarde
        docker cp "$BACKUP_DIR/${BACKUP_NAME}_redis.rdb" bloomzy-redis:/data/dump.rdb
        
        # Redémarrer Redis
        docker compose -f docker-compose.full.yml start redis
        
        echo "✅ Restauration Redis terminée"
    else
        echo "⚠️  Fichier de sauvegarde Redis non trouvé"
    fi
}

# Fonction pour restaurer les volumes
restore_volumes() {
    echo "🔄 Restauration des volumes..."
    
    if [ -f "$BACKUP_DIR/${BACKUP_NAME}_volumes.tar.gz" ]; then
        # Créer le volume s'il n'existe pas
        docker volume create bloomzy_postgres_data
        
        # Restaurer les données
        docker run --rm -v bloomzy_postgres_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar xzf /backup/${BACKUP_NAME}_volumes.tar.gz -C /data
        
        echo "✅ Restauration volumes terminée"
    else
        echo "⚠️  Fichier de sauvegarde volumes non trouvé"
    fi
}

# Fonction pour restaurer la configuration
restore_config() {
    echo "🔄 Restauration de la configuration..."
    
    if [ -f "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz" ]; then
        # Créer un backup de la config actuelle
        tar czf "config_backup_$(date +%Y%m%d_%H%M%S).tar.gz" docker-compose*.yml monitoring/ scripts/ .env* 2>/dev/null || true
        
        # Restaurer la configuration
        tar xzf "$BACKUP_DIR/${BACKUP_NAME}_config.tar.gz"
        
        echo "✅ Restauration configuration terminée"
    else
        echo "⚠️  Fichier de sauvegarde configuration non trouvé"
    fi
}

# Exécuter les restaurations
restore_volumes
restore_postgres
restore_redis
restore_config

# Redémarrer tous les services
echo "🚀 Redémarrage des services..."
docker compose -f docker-compose.full.yml up -d

echo "⏳ Attente du démarrage des services..."
sleep 30

echo "✅ Restauration terminée!"
echo "🌐 Services disponibles:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:5001"
echo "   - Grafana: http://localhost:3001"

# Vérifier l'état des services
docker compose -f docker-compose.full.yml ps