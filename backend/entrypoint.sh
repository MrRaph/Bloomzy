#!/bin/sh
set -e


DB_DIR="/data"
DB_PATH="$DB_DIR/bloomzy.db"

# S'assure que le dossier /data existe
mkdir -p "$DB_DIR"

if [ ! -f "$DB_PATH" ]; then
  echo "Initialisation de la base de données..."
  if flask db upgrade 2>/dev/null; then
    echo "✅ Migrations appliquées (Flask-Migrate)"
  else
    python -c "from app import create_app; app = create_app()"
    echo "✅ Base de données initialisée (sans migrations)"
  fi
else
  echo "Base de données déjà présente, pas d'initialisation nécessaire."
fi

exec "$@"
