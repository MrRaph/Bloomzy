# API Plantes d'Intérieur

## Vue d'ensemble

Cette API gère les plantes d'intérieur avec deux composants principaux :
1. **Catalogue des espèces** : Gestion des espèces de plantes (endpoints publics)
2. **Plantes utilisateur** : Gestion des plantes personnelles (endpoints authentifiés)

## Catalogue des Espèces

### Endpoints publics

#### 1.1 Créer une espèce de plante
- **POST** `/indoor-plants/`
- **Payload JSON** :
```json
{
  "scientific_name": "Sansevieria trifasciata",
  "common_names": "Snake Plant, Langue de belle-mère",
  "family": "Asparagaceae",
  "origin": "Afrique de l'Ouest",
  "difficulty": "Facile",
  "watering_frequency": "Mensuel",
  "light": "Peu lumineux à lumineux",
  "humidity": "Faible à moyenne",
  "temperature": "15-30°C",
  "soil_type": "Drainant",
  "adult_size": "1m",
  "growth_rate": "Lent",
  "toxicity": "Toxique pour animaux",
  "air_purification": true,
  "flowering": "Rare"
}
```
- **Réponse 201** :
```json
{
  "id": 1,
  "scientific_name": "Sansevieria trifasciata",
  ...
}
```

#### 1.2 Lister et rechercher les espèces
- **GET** `/indoor-plants/`
- **Paramètres** :
  - `search` (optionnel) : filtre par nom scientifique
- **Exemple** :
  - `/indoor-plants/?search=Sansevieria`
- **Réponse 200** :
```json
[
  {
    "id": 1,
    "scientific_name": "Sansevieria trifasciata",
    ...
  },
  ...
]
```

## Plantes Utilisateur

Pour la gestion des plantes personnelles des utilisateurs, voir la documentation dédiée :

**📖 [Documentation API Plantes Utilisateur](user_plants_api.md)**

Cette API comprend :
- ✅ **Gestion CRUD** des plantes personnelles
- ✅ **Upload de photos** pour les plantes  
- ✅ **Historique d'arrosage** complet
- ✅ **Authentification JWT** sécurisée
- ✅ **Validation** complète des données
- ✅ **Isolation utilisateur** garantie

### Endpoints principaux
- `GET /api/plants/my-plants` - Lister mes plantes
- `POST /api/plants/my-plants` - Créer une plante
- `POST /api/plants/my-plants/{id}/photo` - Upload photo
- `POST /api/plants/watering` - Enregistrer arrosage
- `GET /api/plants/{id}/watering-history` - Historique arrosage

## Validation du Catalogue
- Tous les champs sont facultatifs sauf `scientific_name` (obligatoire).
- Les champs booléens doivent être au format `true` ou `false`.

## Exemples d'utilisation du Catalogue

### Création d'une espèce
```bash
curl -X POST http://localhost:5080/indoor-plants/ \
  -H "Content-Type: application/json" \
  -d '{"scientific_name": "Sansevieria trifasciata", "air_purification": true}'
```

### Recherche d'espèces
```bash
curl http://localhost:5080/indoor-plants/?search=Sansevieria
```

## Statut Global

### Catalogue des Espèces (Issue #6)
- ✅ **Développement** : Terminé
- ✅ **Tests** : 13 tests passants (100%)
- ✅ **Documentation** : Complète
- ✅ **TDD** : Méthodologie suivie
- ✅ **Référence** : `tests/indoor/test_indoor_plants.py`

### Plantes Utilisateur (Issue #7)
- ✅ **Développement** : Terminé
- ✅ **Tests** : 18 tests passants (100%)
- ✅ **Documentation** : Complète
- ✅ **TDD** : Méthodologie suivie
- ✅ **Sécurité** : Authentification et isolation utilisateur
- ✅ **Référence** : `tests/indoor/test_user_plant.py`, `tests/indoor/test_user_plants_api_simple.py`

## Fichiers de référence

### Code source
- Catalogue : `routes/indoor_plants.py`, `models/indoor_plant.py`
- Plantes utilisateur : `routes/user_plants.py`, `models/user_plant.py`, `models/watering_history.py`

### Tests
- Catalogue : `tests/indoor/test_indoor_plants.py`
- Plantes utilisateur : `tests/indoor/test_user_plant.py`, `tests/indoor/test_user_plants_api_simple.py`

### Documentation
- Catalogue : Ce fichier
- Plantes utilisateur : `user_plants_api.md`
