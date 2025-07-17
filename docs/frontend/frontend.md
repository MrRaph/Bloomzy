# Documentation technique du frontend Bloomzy

## Structure du projet

- **Vue 3 + TypeScript** : Composition API pour modularité et typage strict.
- **Pinia** : Gestion d’état centralisée (auth, indoorPlants, etc.).
- **Axios** : Appels API typés, intercepteurs, mock facile pour les tests.
- **Vite** : Build rapide, configuration simple.
- **Vitest** : TDD systématique, couverture complète (services, stores, vues).

## Organisation des dossiers

- `src/services/api.ts` :
  - Service principal pour les appels API (auth, indoor plants).
  - Utilisation directe d’axios pour faciliter le mock.
  - Typage strict des réponses (ex : `AuthTokens`, `User`).
  - Chaque méthode est testée dans `api.spec.ts`.

- `src/stores/` :
  - Stores Pinia pour chaque domaine (auth, indoorPlants).
  - Tests unitaires pour chaque store (ex : `auth.spec.ts`).
  - Utilisation de localStorage pour la persistance des tokens.

- `src/views/` :
  - Vues principales (Home, Login, Signup, Profile).
  - Tests unitaires pour chaque vue avec @vue/test-utils, Pinia et Router mockés.

- `src/types/` :
  - Types partagés (User, AuthTokens, etc.).

## Bonnes pratiques

- **TDD systématique** : Chaque module (service, store, vue) possède son fichier de test associé.
- **Mocking** :
  - Axios mocké dans les tests de services.
  - Pinia et Vue Router mockés dans les tests de vues.
- **Typage strict** : Tous les appels API et stores utilisent des types TypeScript pour garantir la sécurité et la maintenabilité.
- **Sécurité** :
  - Jamais de secrets hardcodés.
  - Utilisation de localStorage pour les tokens JWT.
  - Validation des entrées côté frontend et backend.

## Exécution des tests

```bash
npm run test -- --environment jsdom
```
- Tous les tests frontend sont exécutés avec jsdom pour simuler le DOM.
- Les tests de vues mockent Pinia et le routeur pour éviter les erreurs d’injection.

## Extension et maintenance

- Ajouter un module : créer le service, le store, la vue et le test associé.
- Pour toute nouvelle fonctionnalité, suivre le process TDD et mettre à jour la documentation.
- Les tests doivent toujours passer avant tout merge ou déploiement.

## Références
- Voir les PRD et TODOs dans le dossier `docs/` pour les spécifications fonctionnelles et techniques.
- Consulter ce fichier et le README du frontend pour les standards de code et la configuration avancée.
