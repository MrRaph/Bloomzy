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

---

Pour toute modification, mettre à jour ce fichier et la documentation associée.
