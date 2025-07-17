# TODO Authentification & Gestion Utilisateur

## Objectif
Développer un système d’authentification sécurisé, complet et personnalisable.

### Étapes
1. **Initialisation du module Auth** ([Issue #1](https://github.com/MrRaph/Bloomzy/issues/1))
   - Créer la branche `feature/auth-init`.
   - Objectif : Structure de base, endpoints REST, modèles DB.
   - Validation : Tests unitaires sur la création d’utilisateur.

2. **Inscription & Connexion (email, OAuth, invité)** ([Issue #2](https://github.com/MrRaph/Bloomzy/issues/2))
   - Développer les endpoints et la logique métier.
   - Objectif : Inscription, connexion, vérification email, gestion des sessions.
   - Validation : Tests d’intégration (inscription, login, refresh, logout).

3. **Gestion du profil utilisateur** ([Issue #3](https://github.com/MrRaph/Bloomzy/issues/3))
   - CRUD profil, préférences, photo, bio.
   - Objectif : API REST, validation des données, sécurité.
   - Validation : Tests unitaires et documentation OpenAPI.

4. **Gestion des clés API IA** ([Issue #4](https://github.com/MrRaph/Bloomzy/issues/4))
   - Stockage sécurisé, test de connexion, rotation.
   - Objectif : Endpoints, chiffrement, monitoring d’usage.
   - Validation : Tests de sécurité, tests d’intégration.

5. **Sécurité avancée** ([Issue #5](https://github.com/MrRaph/Bloomzy/issues/5))
   - MFA, rate limiting, audit trail, RGPD.
   - Objectif : Implémentation, documentation, tests de sécurité.
   - Validation : Couverture >90%, audit automatisé.

### Critères de validation
- 100% des endpoints testés (TDD)
- Documentation OpenAPI à jour
- Fonctionnalités validées par tests d’intégration
- PR sur `main` avec revue et merge
