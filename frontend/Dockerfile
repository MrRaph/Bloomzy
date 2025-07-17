# Dockerfile frontend Bloomzy
# Ce fichier permet de construire l'image Docker pour le frontend Vue.js

FROM node:20-alpine

WORKDIR /app

# Installer wget pour les health checks
RUN apk add --no-cache wget

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install --legacy-peer-deps

# Copier le reste des fichiers
COPY . .

# Définir les variables d'environnement pour le build
ARG VITE_API_URL=http://localhost:5080
ENV VITE_API_URL=$VITE_API_URL

# Builder l'application
RUN npm run build

# Vérifier que le répertoire dist existe
RUN ls -la dist/

EXPOSE 8080

CMD ["npx", "http-server", "dist", "-p", "8080", "--cors"]
