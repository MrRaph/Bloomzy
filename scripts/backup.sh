#!/bin/bash

# Script de sauvegarde automatique pour Bloomzy
# Usage: ./scripts/backup.sh

BACKUP_DIR="backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="bloomzy_backup_$TIMESTAMP"

echo "🔄 Démarrage de la sauvegarde Bloomzy..."

# Créer le répertoire de backup s'il n'existe pas
mkdir -p $BACKUP_DIR

# Fonction pour sauvegarder PostgreSQL
backup_postgres() {
    echo "📦 Sauvegarde de PostgreSQL..."
    
    if docker ps | grep -q "bloomzy-postgres"; then
        docker exec bloomzy-postgres pg_dump -U bloomzy -d bloomzy > "$BACKUP_DIR/${BACKUP_FILE}_postgres.sql"
        echo "✅ Sauvegarde PostgreSQL terminée"
    else
        echo "⚠️  Container PostgreSQL non trouvé, passage de la sauvegarde DB"
    fi
}

# Fonction pour sauvegarder Redis
backup_redis() {
    echo "📦 Sauvegarde de Redis..."
    
    if docker ps | grep -q "bloomzy-redis"; then
        docker exec bloomzy-redis redis-cli SAVE
        docker cp bloomzy-redis:/data/dump.rdb "$BACKUP_DIR/${BACKUP_FILE}_redis.rdb"
        echo "✅ Sauvegarde Redis terminée"
    else
        echo "⚠️  Container Redis non trouvé, passage de la sauvegarde Redis"
    fi
}

# Fonction pour sauvegarder les volumes Docker
backup_volumes() {
    echo "📦 Sauvegarde des volumes Docker..."
    
    # Créer une archive des volumes
    docker run --rm -v bloomzy_postgres_data:/data -v $(pwd)/$BACKUP_DIR:/backup alpine tar czf /backup/${BACKUP_FILE}_volumes.tar.gz -C /data .
    
    echo "✅ Sauvegarde volumes terminée"
}

# Fonction pour sauvegarder les fichiers de configuration
backup_config() {
    echo "📦 Sauvegarde des configurations..."
    
    tar czf "$BACKUP_DIR/${BACKUP_FILE}_config.tar.gz" \
        docker-compose*.yml \
        monitoring/ \
        scripts/ \
        .env* \
        2>/dev/null || echo "⚠️  Certains fichiers de config non trouvés"
    
    echo "✅ Sauvegarde configuration terminée"
}

# Fonction pour nettoyer les anciens backups (garder les 7 derniers)
cleanup_old_backups() {
    echo "🧹 Nettoyage des anciens backups..."
    
    # Garder seulement les 7 derniers backups
    find $BACKUP_DIR -name "bloomzy_backup_*" -type f -printf '%T@ %p\n' | sort -n | head -n -21 | cut -d' ' -f2- | xargs -r rm
    
    echo "✅ Nettoyage terminé"
}

# Exécuter les sauvegardes
backup_postgres
backup_redis
backup_volumes
backup_config
cleanup_old_backups

# Créer un fichier de manifest
cat > "$BACKUP_DIR/${BACKUP_FILE}_manifest.txt" << EOF
Backup Bloomzy - $TIMESTAMP
==============================

Fichiers inclus:
- ${BACKUP_FILE}_postgres.sql (Base de données PostgreSQL)
- ${BACKUP_FILE}_redis.rdb (Cache Redis)
- ${BACKUP_FILE}_volumes.tar.gz (Volumes Docker)
- ${BACKUP_FILE}_config.tar.gz (Fichiers de configuration)

Pour restaurer:
./scripts/restore.sh $BACKUP_FILE
EOF

echo "✅ Sauvegarde complète terminée: $BACKUP_FILE"
echo "📁 Fichiers sauvegardés dans: $BACKUP_DIR/"
ls -la "$BACKUP_DIR/${BACKUP_FILE}_"*