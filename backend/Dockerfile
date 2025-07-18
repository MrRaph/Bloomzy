
FROM python:3.11-slim

# Volume pour la persistance de la base SQLite
VOLUME ["/data"]

# Dockerfile backend Bloomzy
# Ce fichier permet de construire l'image Docker pour le backend Python/Flask

WORKDIR /app

# Installer wget pour les health checks
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copier le reste des fichiers
COPY . .

EXPOSE 5000

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
