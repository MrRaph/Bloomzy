## Utilisation multi-service avec Docker Compose

Le projet Bloomzy propose un déploiement simultané du backend (Flask) et du frontend (Vue.js) via Docker Compose.

### Production

Le fichier `docker-compose.prod.yml` permet de lancer les deux services :

- **backend** :
  - Build à partir de `backend/Dockerfile`
  - Exposé sur le port 5000
  - Variables d’environnement : `FLASK_ENV=production`
- **frontend** :
  - Build à partir de `frontend/Dockerfile`
  - Exposé sur le port 8080
  - Variables d’environnement : `NODE_ENV=production`

Commande pour lancer en production :
```zsh
DOCKER_BUILDKIT=1 docker compose -f docker-compose.prod.yml up --build -d
```

### Développement

Le fichier `docker-compose.dev.yml` permet le hot reload du code et le développement simultané :

- **backend** :
  - Montage du dossier local `backend/` dans le conteneur
  - Variables d’environnement : `FLASK_ENV=development`
- **frontend** :
  - Montage du dossier local `frontend/` dans le conteneur
  - Variables d’environnement : `NODE_ENV=development`

Commande pour lancer en développement :
```zsh
DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up --build
```

### Accès aux services

- Backend : http://localhost:5000
- Frontend : http://localhost:8080

---
# Documentation Dockerfile backend

Ce fichier décrit le Dockerfile utilisé pour construire l’image Docker du backend Bloomzy.

## Objectifs
- Isoler l’environnement Python/Flask dans un conteneur.
- Utiliser le venv local pour l’installation des dépendances.
- Exposer le serveur Flask sur le port 5000.
- Faciliter l’intégration avec Docker Compose et CI/CD.

## Structure du Dockerfile

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/ /app/

RUN python -m venv .venv \
    && . .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000

CMD [".venv/bin/python", "app/__init__.py"]
```

## Emplacement
Le Dockerfile est placé à la racine du projet ou dans le dossier `backend/` selon la structure recommandée.

## Références
 - [docs/backend/best_practices.md](./best_practices.md)
 - [docs/todos/todo_architecture.md](../todos/todo_architecture.md)
 - Issue GitHub : [#26](https://github.com/MrRaph/Bloomzy/issues/26)

## Utilisation des fichiers docker-compose

Deux fichiers sont disponibles à la racine du projet :
- `docker-compose.prod.yml` : pour le déploiement en production
- `docker-compose.dev.yml` : pour le développement local

### Production

```zsh
DOCKER_BUILDKIT=1 docker compose -f docker-compose.prod.yml up --build -d
```
- L’image est construite sans montage de volume, avec les variables d’environnement de production.
- Le conteneur redémarre automatiquement en cas de crash.

### Développement

```zsh
DOCKER_BUILDKIT=1 docker compose -f docker-compose.dev.yml up --build
```
- Le dossier `backend/` est monté dans le conteneur pour un hot reload du code.
- Les variables d’environnement sont adaptées au développement.
- Le conteneur redémarre sauf arrêt manuel.

---
Pour toute modification, mettre à jour ce fichier et la documentation associée.
Pour toute modification, mettre à jour ce fichier et la documentation associée.
