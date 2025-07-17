# Documentation API Keys Management

## Gestion des clés API pour les services d'intelligence artificielle

### Services supportés
- `openai` : OpenAI GPT (format: `sk-...`)
- `claude` : Anthropic Claude (format: `sk-ant-...`)
- `gemini` : Google Gemini (format générique)
- `huggingface` : HuggingFace (format: `hf_...`)

---

## GET /api/keys/services

**Description** : Récupère la liste des services supportés.

**Headers requis** :
- `Authorization: Bearer <token>`

**Réponses** :
- `200 OK` : Liste des services
  - `{ "services": ["openai", "claude", "gemini", "huggingface"] }`
- `401 Unauthorized` : Token manquant ou invalide

---

## GET /api/keys/

**Description** : Liste toutes les clés API de l'utilisateur connecté.

**Headers requis** :
- `Authorization: Bearer <token>`

**Réponses** :
- `200 OK` : Liste des clés API (sans exposer les clés chiffrées)
  - `[{ "id": int, "service_name": string, "key_name": string, "is_active": boolean, "last_used": string|null, "created_at": string, "updated_at": string }]`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Utilisateur non trouvé

---

## POST /api/keys/

**Description** : Crée une nouvelle clé API pour un service.

**Headers requis** :
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Payload JSON requis** :
- `service_name` (string, requis) : Nom du service (openai, claude, gemini, huggingface)
- `api_key` (string, requis) : Clé API au format valide pour le service
- `key_name` (string, requis) : Nom descriptif pour la clé (3-100 caractères)

**Réponses** :
- `201 Created` : Clé API créée avec succès
  - `{ "id": int, "service_name": string, "key_name": string, "is_active": boolean, "created_at": string, "updated_at": string }`
- `400 Bad Request` :
  - Champs manquants
  - Service non supporté
  - Format de clé invalide
  - Nom de clé invalide
  - `{ "error": string }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Utilisateur non trouvé
- `500 Internal Server Error` : Erreur lors de la création

**Cas testés** :
- Création réussie d'une clé API
- Service non supporté
- Format de clé invalide
- Champs manquants
- Remplacement automatique de la clé active existante

---

## GET /api/keys/{id}

**Description** : Récupère les détails d'une clé API spécifique.

**Headers requis** :
- `Authorization: Bearer <token>`

**Paramètres URL** :
- `id` (int) : ID de la clé API

**Réponses** :
- `200 OK` : Détails de la clé API
  - `{ "id": int, "service_name": string, "key_name": string, "is_active": boolean, "last_used": string|null, "created_at": string, "updated_at": string }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Clé API non trouvée ou utilisateur non trouvé

---

## PUT /api/keys/{id}

**Description** : Met à jour une clé API existante.

**Headers requis** :
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Paramètres URL** :
- `id` (int) : ID de la clé API

**Payload JSON optionnel** :
- `key_name` (string) : Nouveau nom descriptif (3-100 caractères)
- `is_active` (boolean) : Activer/désactiver la clé

**Réponses** :
- `200 OK` : Clé API mise à jour
  - `{ "id": int, "service_name": string, "key_name": string, "is_active": boolean, "last_used": string|null, "created_at": string, "updated_at": string }`
- `400 Bad Request` :
  - Données requises manquantes
  - Nom de clé invalide
  - `{ "error": string }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Clé API non trouvée
- `500 Internal Server Error` : Erreur lors de la mise à jour

---

## DELETE /api/keys/{id}

**Description** : Supprime définitivement une clé API.

**Headers requis** :
- `Authorization: Bearer <token>`

**Paramètres URL** :
- `id` (int) : ID de la clé API

**Réponses** :
- `200 OK` : Clé API supprimée
  - `{ "message": "Clé API supprimée" }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Clé API non trouvée
- `500 Internal Server Error` : Erreur lors de la suppression

---

## POST /api/keys/{id}/test

**Description** : Teste la validité d'une clé API auprès du service.

**Headers requis** :
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Paramètres URL** :
- `id` (int) : ID de la clé API

**Réponses** :
- `200 OK` : Test réussi
  - `{ "message": "Clé API fonctionnelle", "status": "success" }`
- `400 Bad Request` :
  - Clé API désactivée
  - Test de connexion échoué
  - `{ "message": string, "status": "error" }`
- `401 Unauthorized` : Token manquant ou invalide
- `404 Not Found` : Clé API non trouvée
- `500 Internal Server Error` : Erreur lors du test

---

## Sécurité

- **Chiffrement** : Toutes les clés API sont chiffrées en base avec `cryptography.fernet`
- **Clé unique** : Un seul clé active par service par utilisateur
- **Validation** : Format de clé validé selon le service
- **Isolation** : Chaque utilisateur n'accède qu'à ses propres clés
- **Audit** : Suivi des dernières utilisations

---

## Cas d'usage

1. **Ajout d'une nouvelle clé OpenAI** :
   ```bash
   POST /api/keys/
   {
     "service_name": "openai",
     "api_key": "sk-1234567890abcdef1234567890abcdef",
     "key_name": "Ma clé OpenAI personnelle"
   }
   ```

2. **Listage des clés** :
   ```bash
   GET /api/keys/
   ```

3. **Désactivation d'une clé** :
   ```bash
   PUT /api/keys/1
   {
     "is_active": false
   }
   ```

4. **Test de connexion** :
   ```bash
   POST /api/keys/1/test
   ```

---

*Cette documentation doit être mise à jour à chaque ajout ou modification d'endpoint.*