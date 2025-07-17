# Dockerfile frontend Bloomzy
# Ce fichier permet de construire l'image Docker pour le frontend Vue.js

FROM node:20-alpine

WORKDIR /app

COPY . /app/

RUN npm install --legacy-peer-deps

RUN npm run build

EXPOSE 8080

CMD ["npx", "http-server", "dist", "-p", "8080"]
