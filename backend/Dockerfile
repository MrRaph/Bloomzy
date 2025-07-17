# Dockerfile backend Bloomzy
# Ce fichier permet de construire l'image Docker pour le backend Python/Flask

FROM python:3.11-slim

WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copier le reste des fichiers
COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
