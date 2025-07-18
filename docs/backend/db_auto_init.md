# Initialisation automatique de la base de données au démarrage du conteneur backend

Depuis juillet 2025, le backend Flask initialise automatiquement la base de données SQLite lors du démarrage du conteneur Docker, si celle-ci n'existe pas encore.

## Fonctionnement

- Le script `entrypoint.sh` (copié dans l'image Docker) vérifie la présence du fichier `/data/bloomzy.db`.
- Si la base n'existe pas, il tente d'abord d'appliquer les migrations (`flask db upgrade`).
- Si Flask-Migrate n'est pas configuré, il crée la base via l'application Flask (`create_app`).
- Si la base existe déjà, aucune action n'est effectuée.
- Le serveur Flask démarre ensuite normalement.

## Utilisation

Aucune action manuelle n'est requise pour initialiser la base de données lors du premier lancement du backend en Docker.

- Pour forcer une réinitialisation, supprimez le fichier `/data/bloomzy.db` (ou le volume associé) puis relancez le conteneur.

## Fichiers concernés
- `backend/entrypoint.sh` : script d'initialisation
- `backend/Dockerfile` : configuration de l'entrypoint
- `.env` et `docker-compose.dev.yml` : configuration du chemin de la DB

## Exemple de log au démarrage
```
Initialisation de la base de données...
✅ Migrations appliquées (Flask-Migrate)
 * Running on http://0.0.0.0:5000
```

## Tests
- Supprimez le fichier `/data/bloomzy.db` puis relancez le conteneur backend : la base doit être créée automatiquement.
- Relancez le conteneur avec la base déjà présente : aucun message d'initialisation ne doit apparaître.

---

Pour toute question, voir la documentation Docker ou contacter l'équipe technique.
