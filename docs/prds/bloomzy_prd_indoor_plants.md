# GrowWise - PRD Gestion Plantes d'Intérieur

## 1. Objectifs

### Objectif principal
Créer un système complet de gestion des plantes d'intérieur avec notifications intelligentes d'arrosage basées sur les données météorologiques et les caractéristiques des plantes.

### Objectifs secondaires
- Faciliter l'entretien quotidien des plantes
- Prévenir la mort des plantes par négligence
- Éduquer les utilisateurs sur les besoins spécifiques
- Créer un journal de croissance visuel

## 2. Fonctionnalités

### 2.1 Catalogue de plantes

#### 2.1.1 Base de données des espèces
- **Informations botaniques**:
  - Nom scientifique et noms communs
  - Famille botanique
  - Origine géographique
  - Niveau de difficulté

- **Besoins d'entretien**:
  - Fréquence d'arrosage (base)
  - Luminosité requise
  - Humidité ambiante
  - Température idéale
  - Type de sol préféré

- **Caractéristiques**:
  - Taille adulte
  - Vitesse de croissance
  - Toxicité (animaux/enfants)
  - Purification d'air
  - Floraison/fructification

#### 2.1.2 Recherche et filtres
- **Recherche par**:
  - Nom (scientifique/commun)
  - Conditions de culture
  - Niveau de difficulté
  - Utilité (décorative, purifiante)

- **Filtres avancés**:
  - Compatible avec animaux
  - Faible luminosité
  - Résistante à la sécheresse
  - Adaptée débutants

### 2.2 Mes plantes

#### 2.2.1 Ajout de plantes
- **Méthodes d'ajout**:
  - Sélection depuis le catalogue
  - Scan de code QR (si disponible)
  - Reconnaissance par photo (IA)
  - Saisie manuelle

- **Informations personnalisées**:
  - Nom personnalisé
  - Localisation dans la maison
  - Date d'acquisition
  - Taille du pot
  - Provenance (magasin, bouture, etc.)

#### 2.2.2 Profil de plante
- **Informations de base**:
  - Photo actuelle
  - Historique des photos
  - Statut de santé
  - Âge estimé

- **Conditions actuelles**:
  - Exposition lumineuse
  - Humidité locale
  - Température ambiante
  - Dernier rempotage

### 2.3 Système d'arrosage intelligent

#### 2.3.1 Algorithme de calcul
- **Facteurs considérés**:
  - Espèce de plante (besoins de base)
  - Saison (métabolisme variable)
  - Météo extérieure (humidité, température)
  - Humidité intérieure estimée
  - Taille du pot
  - Type de substrat
  - Dernier arrosage

- **Sources de données**:
  - API météorologique locale
  - Base de données des espèces
  - Historique d'arrosage utilisateur
  - Capteurs IoT (si disponibles)

#### 2.3.2 Notifications d'arrosage
- **Types de notifications**:
  - Arrosage nécessaire
  - Arrosage recommandé
  - Attention sur-arrosage
  - Rappel d'arrosage oublié

- **Personnalisation**:
  - Horaires préférés
  - Fréquence des rappels
  - Canaux de notification
  - Avance sur les notifications

#### 2.3.3 Enregistrement des arrosages
- **Méthodes d'enregistrement**:
  - Bouton rapide dans notification
  - Interface principale
  - Commande vocale (future)
  - Détection automatique (capteurs)

- **Données collectées**:
  - Date et heure
  - Quantité d'eau
  - Qualité de l'eau utilisée
  - Réaction de la plante
  - Notes personnelles

### 2.4 Calendrier de soins

#### 2.4.1 Planification automatique
- **Tâches récurrentes**:
  - Arrosage personnalisé
  - Fertilisation saisonnière
  - Nettoyage des feuilles
  - Rotation pour exposition
  - Contrôle des parasites

- **Tâches ponctuelles**:
  - Rempotage
  - Taille/élagage
  - Propagation
  - Traitement spécifique

#### 2.4.2 Rappels intelligents
- **Contextualisation**:
  - Basé sur l'espèce
  - Adapté à la saison
  - Personnalisé selon l'historique
  - Priorisation des tâches

- **Flexibilité**:
  - Reporter un soin
  - Marquer comme terminé
  - Ajouter des notes
  - Programmer des rappels

### 2.5 Journal de croissance

#### 2.5.1 Suivi photographique
- **Capture d'images**:
  - Photo régulière automatique
  - Comparaison temporelle
  - Détection des changements
  - Galerie chronologique

- **Analyse visuelle**:
  - Croissance mesurée
  - Santé des feuilles
  - Détection de maladies
  - Évolution des couleurs

#### 2.5.2 Métriques de croissance
- **Mesures physiques**:
  - Hauteur de la plante
  - Envergure des feuilles
  - Nombre de tiges/branches
  - Développement racinaire

- **Indicateurs de santé**:
  - Couleur des feuilles
  - Fermeté des tiges
  - Présence de fleurs/fruits
  - Signes de stress

## 3. Spécifications techniques

### 3.1 Base de données

#### 3.1.1 Modèle des espèces
```sql
plant_species (
    id UUID PRIMARY KEY,
    scientific_name VARCHAR(200) NOT NULL,
    common_names TEXT[],
    family VARCHAR(100),
    care_level VARCHAR(20),
    watering_frequency INTEGER, -- en jours
    light_requirements VARCHAR(50),
    humidity_min INTEGER,
    humidity_max INTEGER,
    temperature_min INTEGER,
    temperature_max INTEGER,
    soil_type VARCHAR(100),
    growth_rate VARCHAR(20),
    max_height INTEGER,
    is_toxic BOOLEAN DEFAULT FALSE,
    air_purifying BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.1.2 Plantes utilisateur
```sql
user_plants (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    species_id UUID REFERENCES plant_species(id),
    custom_name VARCHAR(100),
    location VARCHAR(100),
    pot_size VARCHAR(20),
    soil_type VARCHAR(100),
    acquired_date DATE,
    current_photo_url VARCHAR(500),
    health_status VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.1.3 Historique d'arrosage
```sql
watering_history (
    id UUID PRIMARY KEY,
    plant_id UUID REFERENCES user_plants(id),
    watered_at TIMESTAMP NOT NULL,
    amount_ml INTEGER,
    water_type VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 API Endpoints

#### 3.2.1 Catalogue
```
GET /api/plants/species
GET /api/plants/species/{id}
POST /api/plants/species/search
GET /api/plants/species/filters
```

#### 3.2.2 Mes plantes
```
GET /api/plants/my-plants
POST /api/plants/my-plants
GET /api/plants/my-plants/{id}
PUT /api/plants/my-plants/{id}
DELETE /api/plants/my-plants/{id}
POST /api/plants/my-plants/{id}/photo
```

#### 3.2.3 Arrosage
```
POST /api/plants/watering
GET /api/plants/{id}/watering-schedule
GET /api/plants/{id}/watering-history
PUT /api/plants/watering/{id}
```

### 3.3 Algorithme d'arrosage

#### 3.3.1 Calcul de fréquence
```python
def calculate_watering_schedule(plant, weather_data):
    base_frequency = plant.species.watering_frequency
    
    # Ajustements saisonniers
    season_factor = get_season_factor(datetime.now().month)
    
    # Facteur météorologique
    weather_factor = calculate_weather_factor(weather_data)
    
    # Facteur plante (taille, santé)
    plant_factor = calculate_plant_factor(plant)
    
    # Calcul final
    adjusted_frequency = base_frequency * season_factor * weather_factor * plant_factor
    
    return max(1, min(30, adjusted_frequency))
```

#### 3.3.2 Système de notifications
```python
def generate_watering_notifications():
    for plant in get_user_plants():
        last_watering = get_last_watering(plant)
        next_watering = calculate_next_watering(plant, last_watering)
        
        if should_notify(next_watering):
            send_notification(plant, next_watering)
```

## 4. Expérience utilisateur

### 4.1 Interface principale

#### 4.1.1 Dashboard
- **Vue d'ensemble**:
  - Plantes nécessitant attention
  - Notifications d'arrosage
  - Tâches du jour
  - Météo locale

- **Navigation rapide**:
  - Grille des plantes
  - Filtre par statut
  - Recherche rapide
  - Ajout nouvelle plante

#### 4.1.2 Fiche plante
- **Informations essentielles**:
  - Photo actuelle
  - Statut d'arrosage
  - Prochains soins
  - Évolution récente

- **Actions rapides**:
  - Marquer comme arrosé
  - Prendre une photo
  - Ajouter une note
  - Programmer un soin

### 4.2 Processus d'arrosage

#### 4.2.1 Notification
- **Contenu informatif**:
  - Nom de la plante
  - Localisation
  - Quantité recommandée
  - Raison de l'arrosage

- **Actions disponibles**:
  - Marquer comme fait
  - Reporter d'1 heure
  - Voir les détails
  - Ignorer cette fois

#### 4.2.2 Enregistrement
- **Formulaire simple**:
  - Quantité d'eau
  - Type d'eau
  - Observations
  - Photo optionnelle

- **Validation**:
  - Confirmation visuelle
  - Calcul du prochain arrosage
  - Mise à jour du statut
  - Suggestion d'amélioration

### 4.3 Suivi de croissance

#### 4.3.1 Comparaison temporelle
- **Slider temporel**:
  - Navigation par dates
  - Comparaison côte à côte
  - Mesure des changements
  - Annotations personnalisées

#### 4.3.2 Statistiques
- **Graphiques de croissance**:
  - Évolution de la taille
  - Fréquence d'arrosage
  - Santé globale
  - Corrélation météo

## 5. Intégration IA

### 5.1 Reconnaissance de plantes
- **Identification par photo**:
  - Analyse des feuilles
  - Comparaison avec base
  - Suggestions multiples
  - Validation utilisateur

### 5.2 Diagnostic de santé
- **Analyse des symptômes**:
  - Détection de maladies
  - Carences nutritionnelles
  - Stress hydrique
  - Parasites communs

### 5.3 Conseils personnalisés
- **Recommandations IA**:
  - Amélioration des soins
  - Optimisation placement
  - Calendrier personnalisé
  - Prévention des problèmes

## 6. Tests et validation

### 6.1 Tests algorithme
- **Précision d'arrosage**:
  - Comparaison avec experts
  - Suivi de la santé des plantes
  - Ajustement des paramètres
  - Validation saisonnière

### 6.2 Tests utilisateur
- **Usabilité**:
  - Temps de complétion tâches
  - Taux d'erreur
  - Satisfaction globale
  - Adoption des fonctionnalités

### 6.3 Tests de performance
- **Charge système**:
  - Calcul des notifications
  - Traitement des images
  -