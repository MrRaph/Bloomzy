# Guide GitHub Project & Issues pour Bloomzy

Ce guide explique comment organiser le suivi des tâches et fonctionnalités du projet Bloomzy avec GitHub Project, les issues et les labels.

## 1. Labels d’issue

Utilisez les labels suivants pour catégoriser les issues selon le domaine :
- `auth` : Authentification et sécurité
- `indoor` : Gestion des plantes d’intérieur
- `garden` : Gestion du potager
- `notifications` : Système de notifications
- `ai` : Intégration IA et conseils
- `community` : Fonctionnalités communautaires
- `architecture` : Architecture technique et déploiement

## 2. Création des issues

Pour chaque action à réaliser (voir les fichiers TODOs), créez une issue avec la commande :

```sh
gh issue create --title "<Titre>" --body "<Objectif, validation, critères>" --label "<domaine>"
```
Exemple :
```sh
gh issue create --title "Initialisation du module Auth" --body "Objectif : Structure de base, endpoints REST, modèles DB.\nValidation : Tests unitaires sur la création d’utilisateur.\nCritères : TDD, documentation, PR sur branche dédiée." --label "auth"
```

## 3. Lier les issues au projet GitHub

Pour ajouter une issue au projet "Bloomzy Roadmap" (ID 3) :

```sh
gh project item-add 3 --owner MrRaph --url https://github.com/MrRaph/Bloomzy/issues/<numéro>
```
Exemple :
```sh
gh project item-add 3 --owner MrRaph --url https://github.com/MrRaph/Bloomzy/issues/1
```

## 4. Organisation et suivi

- Placez chaque issue dans la colonne appropriée du projet (Backlog, En cours, Revue, Terminé).
- Utilisez les labels pour filtrer et suivre l’avancement par domaine.
- Reliez chaque PR à son issue pour assurer la traçabilité.

## 5. Bonnes pratiques

- Respectez la structure des branches et des PRs (voir `.github/copilot-instructions.md`).
- Mettez à jour la documentation à chaque merge.
- Utilisez les labels pour faciliter la gestion et la revue.

---

Pour toute question ou problème, consultez les fichiers de référence ou demandez une validation avant d’implémenter.
