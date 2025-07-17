# Documentation API Auth (signup & login)

## POST /auth/signup
Crée un nouvel utilisateur.

### Body JSON
- `email` (str, requis) : Email de l’utilisateur
- `password` (str, requis) : Mot de passe
- `recaptcha_token` (str, requis) : Token reCAPTCHA

### Réponses
- 201 : Utilisateur créé `{id, email}`
- 400 : Champs manquants ou invalides
- 409 : Email déjà existant


## POST /auth/login
Authentifie un utilisateur et retourne un JWT.

### Body JSON
- `email` (str, requis) : Email
- `password` (str, requis) : Mot de passe

### Réponses
- 200 : Connexion réussie `{message, user_id, token}`
- 400 : Champs manquants
- 401 : Identifiants invalides

## POST /auth/refresh
Renouvelle le token JWT.

### Body JSON
- `token` (str, requis) : Token JWT à renouveler

### Réponses
- 200 : Nouveau token `{token}`
- 401 : Token expiré ou invalide

---



## POST /auth/logout
Déconnexion de l’utilisateur et ajout du token JWT à une blacklist côté serveur.

### Body JSON
- `token` (str, requis) : Token JWT à révoquer

### Réponses
- 200 : Déconnexion réussie `{message}`
- 400 : Token requis

## Sécurité JWT
- Lors d’un appel à `/logout`, le token est ajouté à une blacklist en mémoire.
- Tout appel à `/refresh` avec un token blacklisté retourne une erreur 401 `Token révoqué`.
- En production, il est recommandé d’utiliser une solution persistante (Redis, base de données) pour la gestion de la blacklist.
# Documentation API Auth - Endpoints testés

## POST /auth/signup

**Description** : Inscription d’un nouvel utilisateur.

**Payload JSON attendu** :
- `email` (string, requis) : Email de l’utilisateur
- `password` (string, requis) : Mot de passe
- `recaptcha_token` (string, requis) : Token reCAPTCHA pour la protection contre les bots

**Réponses** :
- `201 Created` : Succès, utilisateur créé
  - `{ "id": int, "email": string }`
- `400 Bad Request` :
  - Champs manquants
  - Email invalide
  - Mot de passe trop faible
  - Absence de recaptcha_token
  - `{ "error": string }`
- `409 Conflict` : Email déjà utilisé
  - `{ "error": string }`

**Cas testés** :
- Inscription réussie
- Mot de passe faible
- Email invalide
- Champs manquants
- Email déjà utilisé
- Protection contre les bots

---

*Cette documentation doit être mise à jour à chaque ajout ou modification d’endpoint.*
