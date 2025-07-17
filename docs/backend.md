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
