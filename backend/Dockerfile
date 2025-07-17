# Dockerfile backend Bloomzy
# Ce fichier permet de construire l'image Docker pour le backend Python/Flask

FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "run.py"]
