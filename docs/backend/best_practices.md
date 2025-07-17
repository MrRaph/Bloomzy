# Bonnes pratiques Backend Python/Flask

## Sécurité
- Ne jamais hardcoder la clé secrète JWT : utiliser une variable d’environnement (`os.environ.get('SECRET_KEY')`).
- Hasher les mots de passe avec `pbkdf2:sha256` (Werkzeug).
- Valider le format email avec une regex.
- Retourner des codes HTTP explicites (400, 401, 409, etc.).
- Protéger les endpoints sensibles (auth, user) avec des décorateurs ou blueprints.

## Structure
- Utiliser une factory `create_app()` pour l’application Flask.
- Modulariser le code avec des blueprints (ex : auth, user, admin).
- Séparer la configuration par environnement (dev, test, prod).
- Utiliser SQLAlchemy pour la persistance.
- Placer les modèles dans un fichier dédié (`models.py`).
- Placer les routes dans des blueprints (`routes/auth.py`, etc.).

## Tests
- Utiliser Pytest et des fixtures pour les tests unitaires et d’intégration.
- Tester tous les cas d’erreur et de succès.
- Exécuter les tests dans un environnement isolé (venv).

## Documentation
- Documenter chaque endpoint dans le dossier `docs/backend/`.
- Mettre à jour la documentation à chaque modification.
- Utiliser OpenAPI/Swagger pour la documentation API.

## Configuration
- Utiliser un fichier `.env` pour les variables sensibles.
- Charger la configuration avec `python-dotenv` ou équivalent.

---
*Respecter ces bonnes pratiques garantit la sécurité, la maintenabilité et la scalabilité du backend.*
