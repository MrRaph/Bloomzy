#!/bin/sh
set -e


DB_DIR="/data"
DB_PATH="$DB_DIR/bloomzy.db"

# S'assure que le dossier /data existe
mkdir -p "$DB_DIR"
# Test d'écriture dans /data pour vérifier l'accessibilité du volume
touch "$DB_DIR/.write_test" 2>/dev/null || {
  echo "❌ Erreur : le dossier $DB_DIR n'est pas accessible en écriture. Vérifiez le montage du volume Docker." >&2
  exit 1
}
rm -f "$DB_DIR/.write_test"

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
