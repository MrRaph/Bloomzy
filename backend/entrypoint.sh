#!/bin/sh
set -e


DB_DIR="/data"
DB_PATH="$DB_DIR/bloomzy.db"


# S'assure que le dossier /data existe et attend qu'il soit accessible en écriture
mkdir -p "$DB_DIR"
MAX_WAIT=10
WAIT=0
while ! touch "$DB_DIR/.write_test" 2>/dev/null; do
  WAIT=$((WAIT+1))
  if [ $WAIT -ge $MAX_WAIT ]; then
    echo "❌ Erreur : le dossier $DB_DIR n'est pas accessible en écriture après $MAX_WAIT secondes. Vérifiez le montage du volume Docker." >&2
    exit 1
  fi
  echo "⏳ Attente du montage du volume $DB_DIR... ($WAIT/$MAX_WAIT)"
  sleep 1
done
rm -f "$DB_DIR/.write_test"


# Crée le fichier DB vide si absent (pour éviter l'erreur SQLite)
if [ ! -f "$DB_PATH" ]; then
  touch "$DB_PATH" 2>/dev/null || {
    echo "❌ Erreur : impossible de créer $DB_PATH. Vérifiez les droits sur $DB_DIR." >&2
    exit 1
  }
  echo "Initialisation de la base de données..."
  if flask db upgrade 2>/dev/null; then
    echo "✅ Migrations appliquées (Flask-Migrate)"
  else
    python -c "from app import create_app; app = create_app()"
    echo "✅ Base de données initialisée (sans migrations)"
  fi
else
  # Vérifie que le fichier DB est accessible en écriture
  if ! [ -w "$DB_PATH" ]; then
    echo "❌ Erreur : le fichier $DB_PATH n'est pas accessible en écriture." >&2
    exit 1
  fi
  echo "Base de données déjà présente, pas d'initialisation nécessaire."
fi

exec "$@"
