# PRD – Administration du site Bloomzy

## Objectif
Permettre aux administrateurs de gérer les paramètres globaux du site, les utilisateurs, les contenus, et les intégrations (dont la gestion du recaptcha) via une interface dédiée et sécurisée.

## Fonctionnalités principales

### 1. Tableau de bord admin
- Vue synthétique des statistiques (utilisateurs, contenus, activités)
- Accès rapide aux modules de gestion

### 2. Gestion des utilisateurs
- Liste, recherche, filtrage et export des utilisateurs
- Suspension, suppression, modification des profils
- Attribution de rôles (admin, modérateur, utilisateur)

### 3. Gestion des contenus
- Modération des posts, commentaires, photos
- Suppression, édition, archivage
- Historique des actions modérateurs

### 4. Paramètres globaux du site
- Configuration des variables d’environnement (API, sécurité, etc.)
- Activation/désactivation du recaptcha pour l’inscription
- Gestion des clés API et intégrations externes

### 5. Gestion du recaptcha
- Interface pour renseigner la clé publique et privée
- Activation/désactivation du recaptcha sur les formulaires
- Logs des tentatives de validation

### 6. Logs et audit
- Historique des connexions admin
- Journalisation des actions critiques
- Export des logs

### 7. Sécurité
- Authentification forte pour l’accès admin (2FA, JWT, etc.)
- Gestion des permissions par rôle
- Alertes en cas d’activité suspecte

## Critères de validation
- Accès réservé aux comptes administrateurs
- Toutes les actions critiques sont journalisées
- Interface réactive, sécurisée et documentée
- Tests unitaires et d’intégration pour chaque module
- Documentation technique et utilisateur à jour

## Contraintes techniques
- Backend Python/Flask : nouveaux endpoints sous `/admin` (blueprint dédié)
- Frontend Vue.js : nouvelle vue et routes protégées (`/admin`)
- Respect des standards de sécurité et des bonnes pratiques du projet

## Roadmap
- Sprint 1 : Authentification admin + tableau de bord
- Sprint 2 : Gestion utilisateurs et contenus
- Sprint 3 : Paramètres globaux + recaptcha
- Sprint 4 : Logs, audit et sécurité avancée

---

Ce document doit être mis à jour à chaque évolution de la fonctionnalité d’administration.
