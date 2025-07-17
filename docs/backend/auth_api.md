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
