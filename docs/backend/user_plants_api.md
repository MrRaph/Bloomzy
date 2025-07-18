# API Gestion des Plantes Utilisateur

## Vue d'ensemble

Cette API permet aux utilisateurs de gérer leurs plantes personnelles, incluant la gestion CRUD des plantes, l'upload de photos et le suivi de l'historique d'arrosage.

## Authentification

Tous les endpoints nécessitent une authentification JWT. Incluez le token dans l'header Authorization :

```
Authorization: Bearer <votre-jwt-token>
```

## Endpoints

### 1. Gestion des Plantes Utilisateur

#### 1.1 Lister mes plantes
- **GET** `/api/plants/my-plants`
- **Description** : Récupère toutes les plantes de l'utilisateur connecté
- **Authentification** : Requise
- **Réponse 200** :
```json
{
  "plants": [
    {
      "id": 1,
      "user_id": 1,
      "species_id": 1,
      "custom_name": "Mon Ficus Benjamin",
      "location": "Salon",
      "pot_size": "Moyen",
      "soil_type": "Terreau universel",
      "acquired_date": "2023-01-15",
      "current_photo_url": "/uploads/plants/1_ficus.jpg",
      "health_status": "healthy",
      "notes": "Acheté en pépinière locale",
      "light_exposure": "Lumière indirecte",
      "local_humidity": 65,
      "ambient_temperature": 22,
      "last_repotting": "2023-01-15",
      "created_at": "2023-01-15T10:30:00",
      "updated_at": "2023-01-15T10:30:00",
      "species": {
        "id": 1,
        "scientific_name": "Ficus benjamina",
        "common_names": "Ficus pleureur",
        "family": "Moraceae",
        "difficulty": "Facile"
      }
    }
  ],
  "total": 1
}
```

#### 1.2 Créer une nouvelle plante
- **POST** `/api/plants/my-plants`
- **Description** : Ajoute une nouvelle plante à la collection de l'utilisateur
- **Authentification** : Requise
- **Payload JSON** :
```json
{
  "species_id": 1,
  "custom_name": "Mon Ficus Benjamin",
  "location": "Salon",
  "pot_size": "Moyen",
  "soil_type": "Terreau universel",
  "acquired_date": "2023-01-15",
  "health_status": "healthy",
  "notes": "Acheté en pépinière locale",
  "light_exposure": "Lumière indirecte",
  "local_humidity": 65,
  "ambient_temperature": 22,
  "last_repotting": "2023-01-15"
}
```

**Champs obligatoires :**
- `species_id` : ID de l'espèce (doit exister)
- `custom_name` : Nom personnalisé (max 100 caractères)

**Champs optionnels :**
- `location` : Localisation dans la maison
- `pot_size` : Taille du pot
- `soil_type` : Type de substrat
- `acquired_date` : Date d'acquisition (format YYYY-MM-DD)
- `health_status` : État de santé (healthy, sick, dying, dead)
- `notes` : Notes personnelles
- `light_exposure` : Exposition lumineuse
- `local_humidity` : Humidité locale (0-100)
- `ambient_temperature` : Température ambiante (-20 à 50°C)
- `last_repotting` : Date du dernier rempotage (format YYYY-MM-DD)

- **Réponse 201** : Objet plante créé

#### 1.3 Récupérer une plante spécifique
- **GET** `/api/plants/my-plants/{id}`
- **Description** : Récupère une plante spécifique par son ID
- **Authentification** : Requise
- **Réponse 200** : Objet plante
- **Réponse 404** : Plante non trouvée

#### 1.4 Mettre à jour une plante
- **PUT** `/api/plants/my-plants/{id}`
- **Description** : Met à jour une plante existante
- **Authentification** : Requise
- **Payload JSON** : Mêmes champs que la création (tous optionnels)
- **Réponse 200** : Objet plante mis à jour
- **Réponse 404** : Plante non trouvée

#### 1.5 Supprimer une plante
- **DELETE** `/api/plants/my-plants/{id}`
- **Description** : Supprime une plante et son historique d'arrosage
- **Authentification** : Requise
- **Réponse 200** :
```json
{
  "message": "Plant deleted successfully"
}
```

### 2. Gestion des Photos

#### 2.1 Upload de photo
- **POST** `/api/plants/my-plants/{id}/photo`
- **Description** : Upload une photo pour une plante
- **Authentification** : Requise
- **Content-Type** : multipart/form-data
- **Champ** : `photo` (fichier)
- **Formats supportés** : JPG, JPEG, PNG, GIF
- **Réponse 200** :
```json
{
  "message": "Photo uploaded successfully",
  "photo_url": "/uploads/plants/1_photo.jpg"
}
```

### 3. Gestion de l'Arrosage

#### 3.1 Enregistrer un arrosage
- **POST** `/api/plants/watering`
- **Description** : Enregistre un événement d'arrosage
- **Authentification** : Requise
- **Payload JSON** :
```json
{
  "plant_id": 1,
  "watered_at": "2023-01-15 10:30:00",
  "amount_ml": 250,
  "water_type": "filtered",
  "notes": "Arrosage régulier"
}
```

**Champs obligatoires :**
- `plant_id` : ID de la plante (doit appartenir à l'utilisateur)

**Champs optionnels :**
- `watered_at` : Date/heure d'arrosage (défaut: maintenant)
- `amount_ml` : Quantité d'eau en ml (0-10000)
- `water_type` : Type d'eau (tap, filtered, rainwater, distilled, other)
- `notes` : Notes supplémentaires

- **Réponse 201** : Objet arrosage créé

#### 3.2 Historique d'arrosage
- **GET** `/api/plants/{plant_id}/watering-history`
- **Description** : Récupère l'historique d'arrosage d'une plante
- **Authentification** : Requise
- **Réponse 200** :
```json
{
  "plant_id": 1,
  "watering_history": [
    {
      "id": 1,
      "plant_id": 1,
      "watered_at": "2023-01-15T10:30:00",
      "amount_ml": 250,
      "water_type": "filtered",
      "notes": "Arrosage régulier",
      "created_at": "2023-01-15T10:30:00"
    }
  ],
  "total": 1
}
```

#### 3.3 Modifier un arrosage
- **PUT** `/api/plants/watering/{watering_id}`
- **Description** : Met à jour un enregistrement d'arrosage
- **Authentification** : Requise
- **Payload JSON** : Mêmes champs que la création (tous optionnels)
- **Réponse 200** : Objet arrosage mis à jour

## Validation des Données

### Validation UserPlant
- `custom_name` : Obligatoire, max 100 caractères
- `health_status` : Doit être : healthy, sick, dying, dead
- `local_humidity` : 0-100 si fourni
- `ambient_temperature` : -20 à 50°C si fourni

### Validation WateringHistory
- `watered_at` : Obligatoire si fourni
- `amount_ml` : 0-10000 si fourni
- `water_type` : Doit être : tap, filtered, rainwater, distilled, other

## Gestion des Erreurs

### Codes de statut HTTP
- **200** : Succès
- **201** : Créé avec succès
- **400** : Erreur de validation
- **401** : Non authentifié
- **404** : Ressource non trouvée
- **500** : Erreur serveur

### Format des erreurs
```json
{
  "error": "Message d'erreur",
  "details": ["Erreur de validation 1", "Erreur de validation 2"]
}
```

## Exemples d'utilisation

### Créer une plante
```bash
curl -X POST http://localhost:5080/api/plants/my-plants \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "species_id": 1,
    "custom_name": "Mon Ficus",
    "location": "Salon",
    "health_status": "healthy"
  }'
```

### Lister mes plantes
```bash
curl http://localhost:5080/api/plants/my-plants \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Enregistrer un arrosage
```bash
curl -X POST http://localhost:5080/api/plants/watering \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "plant_id": 1,
    "amount_ml": 250,
    "water_type": "filtered"
  }'
```

### Upload d'une photo
```bash
curl -X POST http://localhost:5080/api/plants/my-plants/1/photo \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "photo=@/path/to/photo.jpg"
```

## Sécurité

- Authentification JWT obligatoire sur tous les endpoints
- Isolation des utilisateurs : chaque utilisateur ne peut accéder qu'à ses propres plantes
- Validation des propriétés sur toutes les opérations
- Prévention des accès croisés entre utilisateurs

## Modèles de Données

### UserPlant
- Représente une plante appartenant à un utilisateur
- Lie les espèces de plantes aux informations personnalisées
- Suit l'état de santé et les conditions environnementales

### WateringHistory
- Enregistre les événements d'arrosage pour les plantes
- Inclut la quantité, le type d'eau et les notes
- Ordonné par date d'arrosage (le plus récent en premier)

## Statut

- ✅ **Développement** : Terminé
- ✅ **Tests** : 18 tests passants (100%)
- ✅ **Documentation** : Complète
- ✅ **TDD** : Méthodologie suivie
- ✅ **Sécurité** : Authentification et isolation utilisateur
- ✅ **Validation** : Validation complète des données

## Fichiers de référence

- Code source : `routes/user_plants.py`
- Modèles : `models/user_plant.py`, `models/watering_history.py`
- Tests : `tests/indoor/test_user_plant.py`, `tests/indoor/test_user_plants_api_simple.py`