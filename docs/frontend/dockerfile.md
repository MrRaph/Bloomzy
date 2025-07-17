# Documentation Dockerfile frontend

Ce fichier décrit le Dockerfile utilisé pour construire l’image Docker du frontend Bloomzy (Vue.js).

## Objectifs
- Isoler l’environnement Node.js/Vue.js dans un conteneur.
- Installer les dépendances via npm.
- Builder l’application pour la production.
- Servir le build statique via http-server sur le port 8080.
- Faciliter l’intégration avec Docker Compose et CI/CD.

## Structure du Dockerfile

```Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY . /app/

RUN npm install --legacy-peer-deps

RUN npm run build

EXPOSE 8080

CMD ["npx", "http-server", "dist", "-p", "8080"]
```

## Emplacement
Le Dockerfile est placé dans le dossier `frontend/`.

## Références
- [docs/frontend.md](../frontend.md)
- [docs/todos/todo_architecture.md](../todos/todo_architecture.md)
- Issue GitHub : [#26](https://github.com/MrRaph/Bloomzy/issues/26)

---

Pour toute modification, mettre à jour ce fichier et la documentation associée.
