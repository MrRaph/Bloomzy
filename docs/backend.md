# Contraintes Backend Python

- Utiliser Python 3.11+
- Framework : Flask
- ORM : SQLAlchemy avec Alembic
- Authentification : JWT avec refresh tokens, multi-facteurs (TOTP/SMS/email)
- API REST documentée avec OpenAPI/Swagger
- Tests obligatoires avec Pytest (TDD)
- Dépendances installées dans un environnement virtuel (venv)
- Structure recommandée :
  - backend/app
  - backend/tests
  - backend/requirements.txt
- Respecter la factorisation et la non-répétition
- Documentation à jour à chaque ajout/modification
- Respect du Git Flow (branche, PR, merge sur main après validation)

## Exécution des tests et gestion des imports

- Pour exécuter les tests Pytest, se placer dans le dossier `backend` :
  ```zsh
  cd backend
  source .venv/bin/activate
  pytest tests/auth/
  ```
- Les imports dans les tests doivent utiliser le chemin relatif (ex : `from app import create_app`).
- Ajouter un fichier `__init__.py` dans chaque dossier pour garantir la reconnaissance des packages Python.
