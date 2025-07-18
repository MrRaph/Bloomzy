# Configuration des Variables d'Environnement

## Fichier .env

Le projet Bloomzy utilise un fichier `.env` pour gérer les variables d'environnement. Ce fichier permet de centraliser la configuration et de la personnaliser selon l'environnement (développement, production, etc.).

## Configuration

### 1. Créer le fichier .env

Si le fichier `.env` n'existe pas, copiez le fichier exemple :

```bash
cp .env.example .env
```

### 2. Variables disponibles

| Variable | Description | Valeur par défaut | Exemple |
|----------|-------------|-------------------|---------|
| `SQLALCHEMY_DATABASE_URI` | URL de connexion à la base de données | `sqlite:////data/bloomzy.db` | `mysql://user:pass@host/db` |
| `SECRET_KEY` | Clé secrète Flask pour les sessions | `dev-secret-key-change-in-production` | `your-secure-key-here` |
| `VITE_API_URL` | URL de l'API backend pour le frontend | `http://localhost:5080` | `https://api.bloomzy.com` |
| `NODE_ENV` | Environnement Node.js | `development` | `production` |

### 3. Exemples de configuration

#### Développement (SQLite)
```env
SQLALCHEMY_DATABASE_URI=sqlite:////data/bloomzy.db
SECRET_KEY=dev-secret-key
VITE_API_URL=http://localhost:5080
NODE_ENV=development
```

#### Production (MySQL)
```env
SQLALCHEMY_DATABASE_URI=mysql://username:password@localhost/bloomzy_db
SECRET_KEY=your-very-secure-production-key
VITE_API_URL=https://api.bloomzy.com
NODE_ENV=production
```

## Utilisation avec Docker

Les fichiers `docker-compose.dev.yml` et `docker-compose.prod.yml` sont configurés pour charger automatiquement le fichier `.env` :

```yaml
services:
  backend:
    env_file:
      - .env
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
```

## Sécurité

⚠️ **Important** : Le fichier `.env` contient des informations sensibles et ne doit **jamais** être commité dans le dépôt git.

- Le fichier `.env` est exclu du suivi git via `.gitignore`
- Utilisez `.env.example` comme template pour documenter les variables nécessaires
- En production, utilisez des valeurs sécurisées pour `SECRET_KEY` et autres secrets

## Bonnes pratiques

1. **Développement** : Utilisez SQLite pour simplifier la configuration
2. **Production** : Utilisez MySQL/PostgreSQL pour de meilleures performances
3. **Secrets** : Générez des clés secrètes uniques pour chaque environnement
4. **Documentation** : Mettez à jour `.env.example` lors de l'ajout de nouvelles variables

## Commandes utiles

```bash
# Redémarrer les conteneurs après modification du .env
make docker-stop
make docker-run

# Ou manuellement
docker compose -f docker-compose.dev.yml down
docker compose -f docker-compose.dev.yml up -d
```
