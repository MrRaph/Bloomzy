# API Plantes d’Intérieur

## Endpoints

### 1. Créer une espèce de plante
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

### 2. Lister et rechercher les espèces
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

## Validation
- Tous les champs sont facultatifs sauf `scientific_name` (obligatoire).
- Les champs booléens doivent être au format `true` ou `false`.

## Exemples d’utilisation

### Création
```bash
curl -X POST http://localhost:5001/indoor-plants/ \
  -H "Content-Type: application/json" \
  -d '{"scientific_name": "Sansevieria trifasciata", "air_purification": true}'
```

### Recherche
```bash
curl http://localhost:5001/indoor-plants/?search=Sansevieria
```

## Statut
- TDD, endpoints et tests validés
- Voir aussi : [tests/indoor/test_indoor_plants.py]
