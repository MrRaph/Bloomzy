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

---

**Pour toute nouvelle fonctionnalité, suivre le process décrit dans les TODOs et valider la conformité avec les PRDs.**


## 5. Workflow GitHub Project & Issues

Le workflow complet de gestion des issues, du projet et des PRs est détaillé dans le guide :

- [docs/gh.md](../docs/gh.md)

Merci de vous y référer pour toutes les étapes : création du projet, création et organisation des issues, passage en "In Progress", création de branche, PR, liaison des issues aux PRs, et bonnes pratiques.
