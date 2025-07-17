# Dockerfile backend Bloomzy
# Ce fichier permet de construire l'image Docker pour le backend Python/Flask

FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN python -m venv .venv \
    && . .venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000

CMD [".venv/bin/python", "app/__init__.py"]
