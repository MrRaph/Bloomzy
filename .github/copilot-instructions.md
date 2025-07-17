# Copilot Instructions pour le projet Bloomzy

Ce fichier est destiné à tous les agents Copilot qui interviendront sur ce projet. Il centralise les informations essentielles pour garantir la cohérence, la qualité et la rapidité d’exécution des tâches.

## 1. Structure des documents de référence

### PRDs (Product Requirement Documents)
Les spécifications fonctionnelles et techniques sont détaillées dans les fichiers suivants :
- `docs/prds/bloomzy_prd_general.md`
- `docs/prds/bloomzy_prd_architecture.md`
- `docs/prds/bloomzy_prd_auth.md`
- `docs/prds/bloomzy_prd_community.md`
- `docs/prds/bloomzy_prd_garden.md`
- `docs/prds/bloomzy_prd_indoor_plants.md`
- `docs/prds/bloomzy_prd_notifications.md`
- `docs/prds/bloomzy_prd_ai_integration.md`

### Contraintes techniques
- Backend Python : `docs/backend.md`
- Frontend Vue.js : `docs/frontend.md`

### TODOs
Les étapes de développement, validation et documentation sont listées dans :
- `docs/todos/todo_auth.md`
- `docs/todos/todo_indoor_plants.md`
- `docs/todos/todo_garden.md`
- `docs/todos/todo_notifications.md`
- `docs/todos/todo_ai_integration.md`
- `docs/todos/todo_community.md`
- `docs/todos/todo_architecture.md`

## 2. Méthodologie de développement
- **Test Driven Development (TDD)** obligatoire : chaque fonctionnalité doit être testée avant d’être considérée comme terminée.
- **Factorisation et non-répétition** : mutualiser le code et les tests dès que possible.
- **Documentation** : chaque endpoint, module ou fonctionnalité doit être documenté (OpenAPI, README, etc.).
- **Git Flow strict** : création de branches par fonctionnalité, PR obligatoire, revue et merge sur `main` uniquement après validation.

## 3. Critères de validation
- Fonctionnalité considérée comme terminée si :
  - Elle est testée (unitaires + intégration)
  - Elle est fonctionnelle
  - Elle est documentée
  - Elle a fait l’objet d’une PR et d’une revue

## 4. Conseils pour les agents
- Toujours commencer par consulter les fichiers PRD et TODO avant toute modification ou ajout.
- Respecter la structure des branches et des PRs.
- Utiliser les outils et frameworks recommandés dans les PRDs.
- Mettre à jour la documentation à chaque ajout ou modification significative.
- En cas de doute, demander une validation ou clarification avant d’implémenter.

## 8. Automatisation et bonnes pratiques
- Utiliser le Makefile du backend (`backend/Makefile`) pour automatiser la création du venv, l’installation des dépendances et l’exécution des tests. Voir la documentation associée dans `docs/backend/makefile.md`.
- Consulter et mettre à jour le fichier des bonnes pratiques backend dans `docs/backend/best_practices.md` pour garantir la qualité, la sécurité et la maintenabilité du code Python/Flask.

## 7. Environnement virtuel Python (backend)

- Créer le venv dans le dossier `backend/.venv` :
  ```zsh
  python3 -m venv backend/.venv
  source backend/.venv/bin/activate
  pip install -r backend/requirements.txt
  ```
- Exclure le dossier `backend/.venv/` du suivi git via `.gitignore`.
- Toujours installer les dépendances Python dans ce venv pour garantir l’isolation du projet.

---

**Pour toute nouvelle fonctionnalité, suivre le process décrit dans les TODOs et valider la conformité avec les PRDs.**


## 5. Workflow GitHub Project & Issues

Le workflow complet de gestion des issues, du projet et des PRs est détaillé dans le guide :

- [docs/gh.md](../docs/gh.md)

Merci de vous y référer pour toutes les étapes : création du projet, création et organisation des issues, passage en "In Progress", création de branche, PR, liaison des issues aux PRs, et bonnes pratiques.


## 6. Utilisation de la CLI GitHub (gh)

Pour faciliter la gestion et la vérification des issues, labels et projets, utilisez la CLI GitHub (`gh`). Voici les commandes utiles :

- **Lister toutes les issues du projet** :
  ```zsh
  gh issue list --repo MrRaph/Bloomzy
  ```
- **Lister les issues par label** :
  ```zsh
  gh issue list --repo MrRaph/Bloomzy --label auth,indoor,garden,notifications,ai,community,architecture
  ```
- **Lister les projets du propriétaire** :
  ```zsh
  gh project list --owner MrRaph
  ```
- **Lister les items du projet "Bloomzy Roadmap" (ID 3)** :
  ```zsh
  gh project item-list 3 --owner MrRaph
  ```
- **Afficher le détail d’une issue** :
  ```zsh
  gh issue view <numéro_issue> --repo MrRaph/Bloomzy
  ```

Ces commandes permettent de vérifier rapidement l'état d'initialisation et le suivi du projet sur GitHub.

## 9. Déploiement Docker

### Commandes de développement
```bash
# Installation et build
make install              # Installe toutes les dépendances (backend + frontend)
make docker-build        # Build les images Docker
make docker-run          # Démarre les conteneurs (frontend: localhost:8080, backend: localhost:5080)
make docker-stop         # Arrête les conteneurs
make docker-logs         # Affiche les logs

# Commandes manuelles
docker compose -f docker-compose.dev.yml up -d     # Démarre conteneurs développement
docker compose -f docker-compose.dev.yml down      # Arrête conteneurs développement
docker compose -f docker-compose.dev.yml build     # Build images développement
docker compose -f docker-compose.dev.yml logs -f   # Suit les logs en temps réel
```

### Commandes de production
```bash
docker compose -f docker-compose.prod.yml up -d    # Démarre conteneurs production
docker compose -f docker-compose.prod.yml down     # Arrête conteneurs production
docker compose -f docker-compose.prod.yml build    # Build images production
```

### URLs des services
- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:5080
- **Test endpoint protégé**: http://localhost:5080/auth/protected

### Architecture Docker
- **Frontend**: Vue.js buildé et servi via http-server sur port 8080 (exposé 8080)
- **Backend**: Flask sur port 5000 (exposé 5080)
- **Variables d'environnement**:
  - `VITE_API_URL`: URL de l'API backend pour le frontend
  - `FLASK_ENV` et `FLASK_DEBUG`: Configuration environnement backend
- **Réseau**: Docker network `bloomzy_default` pour la communication inter-services

### Résolution des problèmes courants
1. **Conflit de ports**: Le backend utilise le port 5080 (5000 occupé par AirPlay sur macOS)
2. **Échec du build frontend**: Vérifier que le répertoire `dist/` existe après build
3. **Échec des appels API**: Vérifier la variable d'environnement `VITE_API_URL`
4. **Problèmes de base de données**: Vérifier les permissions du fichier SQLite

### Commandes de debug
```bash
# Vérifier l'état des conteneurs
docker ps

# Voir les logs d'un conteneur
docker logs bloomzy-backend-1

# Accéder au shell d'un conteneur
docker exec -it bloomzy-backend-1 /bin/bash

# Tester l'API directement
curl http://localhost:5080/auth/protected
```

## 10. Standards de code

### Backend (Flask)
- Utiliser le pattern Flask application factory
- Organiser les routes dans des blueprints sous `backend/routes/`
- Modèles dans `backend/models/`
- Authentification JWT avec PyJWT
- Tests dans `backend/tests/` organisés par fonctionnalité

### Frontend (Vue.js)
- Vue 3 Composition API avec TypeScript
- Pinia pour la gestion d'état
- Axios pour les appels API avec intercepteurs
- Configuration API dans `frontend/src/services/api.ts`

### Sécurité
- Jamais de secrets hardcodés (utiliser les variables d'environnement)
- Tokens JWT avec expiration et mécanisme de refresh
- CORS configuré pour les requêtes cross-origin
- Validation des entrées sur tous les endpoints
- Hachage des mots de passe avec Werkzeug

## 11. Documentation technique

- `CLAUDE.md`: Guide de développement complet
- `docs/docker-deployment.md`: Documentation complète du déploiement Docker
- `docs/prds/`: Documents d'exigences produit (consulter avant modifications)
- `docs/todos/`: Tâches de développement organisées par fonctionnalité
