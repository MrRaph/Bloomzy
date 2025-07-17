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

---

## GET /auth/profile

**Description** : Récupération du profil utilisateur connecté.

**Headers requis** :
- `Authorization: Bearer <token>`

**Réponses** :
- `200 OK` : Profil utilisateur
  - `{ "id": int, "email": string, "username": string, "first_name": string, "last_name": string, "bio": string, "profile_picture": string, "location": string, "timezone": string, "language": string, "notifications_enabled": boolean, "email_notifications": boolean, "created_at": string, "updated_at": string, "is_active": boolean }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Utilisateur non trouvé

**Cas testés** :
- Récupération réussie du profil
- Accès sans token
- Token invalide

---

## PUT /auth/profile

**Description** : Mise à jour du profil utilisateur connecté.

**Headers requis** :
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Payload JSON optionnel** :
- `username` (string) : Nom d'utilisateur (3-80 caractères, unique)
- `first_name` (string) : Prénom
- `last_name` (string) : Nom
- `bio` (string) : Biographie (max 500 caractères)
- `location` (string) : Localisation
- `timezone` (string) : Fuseau horaire
- `language` (string) : Langue
- `notifications_enabled` (boolean) : Notifications activées
- `email_notifications` (boolean) : Notifications par email

**Réponses** :
- `200 OK` : Profil mis à jour
  - `{ profil_utilisateur_complet }`
- `400 Bad Request` :
  - Données requises manquantes
  - Username trop court/long
  - Bio trop longue
  - `{ "error": string }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Utilisateur non trouvé
- `409 Conflict` : Username déjà utilisé
- `500 Internal Server Error` : Erreur lors de la mise à jour

**Cas testés** :
- Mise à jour réussie du profil
- Mise à jour des préférences
- Username déjà utilisé
- Username invalide (trop court)
- Bio trop longue
- Mise à jour avec données vides

---

*Cette documentation doit être mise à jour à chaque ajout ou modification d'endpoint.*
