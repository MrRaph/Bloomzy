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

Avant de créer une issue, vérifiez d'abord si elle existe déjà dans le dépôt :
```zsh
gh issue list --repo MrRaph/Bloomzy --json number,title,labels | jq
```
Vous pouvez filtrer par mot-clé ou label avec jq pour vérifier l'existence d'une issue.
Si l'issue existe, utilisez-la. Sinon, créez-la avec la commande suivante :
```sh
gh issue create --title "<Titre>" --body "<Objectif, validation, critères>" --label "<domaine>"
```
Exemple :
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
- Lorsqu'un développement commence, passez l'issue en "In Progress" (En cours) dans le projet.
- Créez une branche dédiée pour le développement (ex : `feature/<nom>`).
- Créez une Pull Request (PR) liée à la branche et à l'issue :
  ```sh
  gh pr create --fill --base main --head feature/<nom> --title "Implémentation : ..." --body "Closes #numéro_issue"
  ```
- Liez l'issue à la PR (GitHub le fait automatiquement si le corps de la PR contient `Closes #numéro_issue`).
- Suivez l'avancement dans le projet et déplacez la carte dans la colonne correspondante (Revue, Terminé).
- Utilisez les labels pour filtrer et suivre l’avancement par domaine.
- Reliez chaque PR à son issue pour assurer la traçabilité.

### Exemple de workflow réel (CLI + Web)

1. **Création de la branche dédiée**
2. **Création de la PR liée à l'issue**
   - Utiliser la commande :
     ```zsh
     gh pr create --fill --base main --head feature/auth-init --title "Implémentation : Initialisation du module Auth" --body "Closes #1\nStructure backend Flask, endpoints Auth, tests TDD, Makefile, documentation et bonnes pratiques."
     ```
   - La PR est automatiquement liée à l'issue grâce au champ `Closes #1`.
3. **Ajout d'un commentaire de progression sur l'issue**
   - Utiliser la commande :
     ```zsh
     gh issue comment 1 --repo MrRaph/Bloomzy --body "Progression : ..."
     ```
   - Permet de documenter l'avancement et la traçabilité.
4. **Déplacement de l'item dans le projet GitHub**
   - La commande CLI pour déplacer l'item dans la colonne "En cours" (`gh project item-move ...`) n'est pas fonctionnelle avec les flags `--owner` ou `--id` (erreur CLI).
   - Solution : effectuer le déplacement manuellement via l'interface web GitHub Project.

**Remarque :**
La liaison PR/issue fonctionne parfaitement via la CLI, mais la gestion des colonnes du projet nécessite souvent une action manuelle sur l'interface web, en raison des limitations ou changements de la CLI GitHub.

## 5. Bonnes pratiques

- Respectez la structure des branches et des PRs (voir `.github/copilot-instructions.md`).
- Mettez à jour la documentation à chaque merge.
- Utilisez les labels pour faciliter la gestion et la revue.

---

Pour toute question ou problème, consultez les fichiers de référence ou demandez une validation avant d’implémenter.


## 6. Utilisation de la CLI GitHub (gh)

Pour gérer et vérifier efficacement les issues, labels et projets, utilisez la CLI GitHub (`gh`). Voici les commandes recommandées :

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

Ces commandes permettent de vérifier à tout moment l’état d’initialisation et le suivi du projet sur GitHub.
