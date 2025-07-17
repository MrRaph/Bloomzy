# GrowWise - PRD Gestion du Potager

## 1. Objectifs

### Objectif principal
Créer un système complet de planification et suivi du potager permettant d'optimiser les cultures, prédire les récoltes et maximiser les rendements.

### Objectifs secondaires
- Planifier les semis selon les conditions climatiques
- Optimiser l'occupation de l'espace au potager
- Suivre l'évolution des cultures en temps réel
- Analyser les performances et améliorer les pratiques

## 2. Fonctionnalités

### 2.1 Catalogue des légumes et cultures

#### 2.1.1 Base de données des variétés
- **Informations botaniques**:
  - Nom scientifique et variétés
  - Famille botanique
  - Origine et sélection
  - Caractéristiques génétiques

- **Cycle de culture**:
  - Période de semis (intérieur/extérieur)
  - Durée de germination
  - Temps avant repiquage
  - Durée totale jusqu'à récolte
  - Période de récolte

- **Besoins culturaux**:
  - Zone de rusticité
  - Température optimale
  - Exposition solaire
  - Besoins en eau
  - Type de sol préféré
  - Besoins nutritionnels

#### 2.1.2 Associations et rotations
- **Compagnonnage**:
  - Plantes compagnes bénéfiques
  - Plantes à éviter
  - Effets sur la croissance
  - Protection naturelle

- **Rotation des cultures**:
  - Famille botanique
  - Besoins nutritionnels
  - Maladies communes
  - Cycles de rotation recommandés

### 2.2 Planification des cultures

#### 2.2.1 Calendrier de semis
- **Calcul automatique**:
  - Basé sur la zone climatique
  - Dernière gelée locale
  - Données météorologiques historiques
  - Preferences utilisateur

- **Types de semis**:
  - Semis direct en pleine terre
  - Semis en intérieur/serre
  - Semis en pépinière
  - Plantation de plants achetés

#### 2.2.2 Planification spatiale
- **Gestion de l'espace**:
  - Dimensions du potager
  - Division en parcelles/carrés
  - Espacement entre plants
  - Calcul de la capacité

- **Optimisation**:
  - Succession de cultures
  - Cultures intercalaires
  - Maximisation des rendements
  - Réduction des espaces vides

### 2.3 Suivi des cultures

#### 2.3.1 Gestion des semis
- **Enregistrement**:
  - Date de semis
  - Variété et quantité
  - Localisation (intérieur/extérieur)
  - Conditions de semis
  - Taux de germination

- **Suivi de développement**:
  - Émergence des plantules
  - Croissance végétative
  - Développement racinaire
  - Préparation au repiquage

#### 2.3.2 Transplantation et repiquage
- **Planification**:
  - Date optimale de repiquage
  - Conditions météorologiques
  - Préparation du sol
  - Espacement final

- **Suivi post-repiquage**:
  - Taux de survie
  - Adaptation au terrain
  - Croissance après transplantation
  - Soins spécifiques

#### 2.3.3 Cycle de croissance
- **Étapes de développement**:
  - Germination
  - Croissance végétative
  - Floraison
  - Fructification
  - Maturation

- **Prédictions**:
  - Dates de récolte prévisionnelles
  - Rendement estimé
  - Qualité attendue
  - Fenêtre de récolte optimale

### 2.4 Gestion des récoltes

#### 2.4.1 Planification des récoltes
- **Calendrier prévisionnel**:
  - Basé sur les dates de semis
  - Ajusté selon les conditions
  - Priorisation des cultures
  - Échelonnement des récoltes

- **Préparation**:
  - Outils nécessaires
  - Containers de stockage
  - Méthodes de conservation
  - Planning des activités

#### 2.4.2 Enregistrement des récoltes
- **Données collectées**:
  - Date et heure de récolte
  - Quantité (poids/volume)
  - Qualité des produits
  - Conditions de récolte
  - Destination (consommation/vente/don)

- **Évaluation qualitative**:
  - Aspect visuel
  - Goût et texture
  - Calibre et uniformité
  - Défauts ou maladies

### 2.5 Analyse des performances

#### 2.5.1 Statistiques de production
- **Rendements**:
  - Par culture et variété
  - Par surface cultivée
  - Par saison
  - Comparaison avec prévisions

- **Efficacité**:
  - Ratio semis/récolte
  - Productivité par m²
  - Coût de production
  - Rentabilité des cultures

#### 2.5.2 Historique et tendances
- **Évolution temporelle**:
  - Performances annuelles
  - Adaptation aux conditions
  - Amélioration des techniques
  - Sélection des variétés

- **Analyse comparative**:
  - Comparaison entre variétés
  - Influence des conditions météo
  - Impact des pratiques culturales
  - Benchmarking avec autres jardiniers

## 3. Spécifications techniques

### 3.1 Base de données

#### 3.1.1 Catalogue des cultures
```sql
vegetable_varieties (
    id UUID PRIMARY KEY,
    scientific_name VARCHAR(200),
    common_name VARCHAR(100),
    variety_name VARCHAR(100),
    plant_family VARCHAR(100),
    hardiness_zone VARCHAR(10),
    days_to_germination INTEGER,
    days_to_transplant INTEGER,
    days_to_harvest INTEGER,
    growing_season VARCHAR(50),
    sun_requirements VARCHAR(50),
    water_needs VARCHAR(50),
    soil_type VARCHAR(100),
    spacing_cm INTEGER,
    depth_cm INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.1.2 Planification des cultures
```sql
garden_plots (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(100),
    length_cm INTEGER,
    width_cm INTEGER,
    soil_type VARCHAR(100),
    sun_exposure VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

planting_plans (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    plot_id UUID REFERENCES garden_plots(id),
    variety_id UUID REFERENCES vegetable_varieties(id),
    planned_sowing_date DATE,
    planned_transplant_date DATE,
    planned_harvest_date DATE,
    quantity_planned INTEGER,
    spacing_cm INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.1.3 Suivi des cultures
```sql
plantings (
    id UUID PRIMARY KEY,
    plan_id UUID REFERENCES planting_plans(id),
    actual_sowing_date DATE,
    sowing_method VARCHAR(50),
    seeds_planted INTEGER,
    germination_rate DECIMAL(5,2),
    transplant_date DATE,
    plants_transplanted INTEGER,
    survival_rate DECIMAL(5,2),
    status VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.1.4 Récoltes
```sql
harvests (
    id UUID PRIMARY KEY,
    planting_id UUID REFERENCES plantings(id),
    harvest_date DATE,
    quantity_kg DECIMAL(8,2),
    quality_rating INTEGER,
    notes TEXT,
    weather_conditions VARCHAR(100),
    storage_method VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 API Endpoints

#### 3.2.1 Catalogue et planification
```
GET /api/garden/varieties
GET /api/garden/varieties/{id}
POST /api/garden/varieties/search
GET /api/garden/plots
POST /api/garden/plots
GET /api/garden/planning/calendar
POST /api/garden/planning/optimize
```

#### 3.2.2 Suivi des cultures
```
GET /api/garden/plantings
POST /api/garden/plantings
GET /api/garden/plantings/{id}
PUT /api/garden/plantings/{id}
POST /api/garden/plantings/{id}/update-status
```

#### 3.2.3 Récoltes
```
GET /api/garden/harvests
POST /api/garden/harvests
GET /api/garden/harvests/statistics
GET /api/garden/harvests/forecast
```

### 3.3 Algorithmes de planification

#### 3.3.1 Calcul des dates optimales
```python
def calculate_optimal_sowing_date(variety, location, year):
    # Récupération des données climatiques
    climate_data = get_climate_data(location)
    last_frost_date = get_average_last_frost(location)
    
    # Calcul basé sur les besoins de la variété
    if variety.is_frost_hardy:
        optimal_date = last_frost_date - timedelta(days=variety.frost_tolerance)
    else:
        optimal_date = last_frost_date + timedelta(days=14)
    
    # Ajustement selon les conditions actuelles
    weather_forecast = get_weather_forecast(location)
    if weather_forecast.indicates_early_season():
        optimal_date -= timedelta(days=7)
    
    return optimal_date
```

#### 3.3.2 Optimisation spatiale
```python
def optimize_garden_layout(plot, selected_varieties):
    # Algorithme de placement optimal
    layout = GardenLayout(plot.dimensions)
    
    # Tri par priorité (rendement, préférences utilisateur)
    sorted_varieties = sort_by_priority(selected_varieties)
    
    for variety in sorted_varieties:
        best_position = find_best_position(layout, variety)
        if best_position:
            layout.place(variety, best_position)
    
    return layout
```

### 3.4 Prédictions et analyses

#### 3.4.1 Prédiction de récolte
```python
def predict_harvest_date(planting, weather_data):
    base_days = planting.variety.days_to_harvest
    sowing_date = planting.actual_sowing_date
    
    # Facteurs d'ajustement
    temperature_factor = calculate_temperature_effect(weather_data)
    moisture_factor = calculate_moisture_effect(weather_data)
    soil_factor = calculate_soil_effect(planting.plot.soil_type)
    
    adjusted_days = base_days * temperature_factor * moisture_factor * soil_factor
    
    return sowing_date + timedelta(days=adjusted_days)
```

#### 3.4.2 Analyse des rendements
```python
def analyze_yield_performance(user_id, season):
    harvests = get_user_harvests(user_id, season)
    
    analysis = {
        'total_yield': sum(h.quantity_kg for h in harvests),
        'yield_per_variety': group_by_variety(harvests),
        'productivity_per_m2': calculate_productivity(harvests),
        'quality_distribution': analyze_quality(harvests),
        'improvement_suggestions': generate_suggestions(harvests)
    }
    
    return analysis
```

## 4. Expérience utilisateur

### 4.1 Interface de planification

#### 4.1.1 Calendrier visuel
- **Vue mensuelle/saisonnière**:
  - Semis planifiés
  - Transplantations
  - Récoltes prévues
  - Tâches d'entretien

- **Glisser-déposer**:
  - Modification des dates
  - Réorganisation des cultures
  - Ajout rapide d'activités
  - Duplication de plannings

#### 4.1.2 Planificateur de potager
- **Vue 2D du potager**:
  - Représentation à l'échelle
  - Drag & drop des cultures
  - Visualisation des associations
  - Calcul automatique des espacements

- **Outils de dessin**:
  - Création de parcelles
  - Modification des dimensions
  - Ajout d'éléments fixes
  - Importation de plans existants

### 4.2 Suivi en temps réel

#### 4.2.1 Dashboard du potager
- **Aperçu global**:
  - Statut des cultures actuelles
  - Tâches urgentes
  - Prochaines récoltes
  - Alertes et notifications

- **Métriques clés**:
  - Taux de germination
  - Croissance moyenne
  - Rendement cumulé
  - Productivité par zone

#### 4.2.2 Fiche de culture
- **Informations détaillées**:
  - Photos d'évolution
  - Mesures de croissance
  - Conditions d'élevage
  - Historique des soins

- **Actions rapides**:
  - Mise à jour du statut
  - Ajout de photos
  - Enregistrement de soins
  - Planification de récolte

### 4.3 Gestion des récoltes

#### 4.3.1 Interface de récolte
- **Saisie simplifiée**:
  - Sélection rapide des cultures
  - Pesée intégrée (si balance connectée)
  - Évaluation qualitative
  - Notes et observations

- **Traçabilité**:
  - Code de lot automatique
  - Conditions de récolte
  - Destination des produits
  - Méthode de conservation

#### 4.3.2 Tableaux de bord analytiques
- **Graphiques de performance**:
  - Évolution des rendements
  - Comparaison variétés
  - Analyse saisonnière
  - Tendances pluriannuelles

- **Rapports personnalisés**:
  - Export des données
  - Analyse comparative
  - Recommandations d'amélioration
  - Planification future

## 5. Intégration météorologique

### 5.1 Données climatiques
- **Historique météo**:
  - Températures moyennes
  - Précipitations
  - Heures d'ensoleillement
  - Dates de gel

- **Prévisions**:
  - Conditions à 15 jours
  - Alertes météorologiques
  - Indices de stress hydrique
  - Prévisions saisonnières

### 5.2 Adaptation des cultures
- **Ajustements automatiques**:
  - Décalage des semis
  - Modification des recommandations
  - Alertes de protection
  - Optimisation de l'irrigation

## 6. Fonctionnalités avancées

### 6.1 Intelligence artificielle
- **Reconnaissance d'images**:
  - Identification des maladies
  - Évaluation de maturité
  - Estimation des rendements
  - Détection des carences

- **Recommandations personnalisées**:
  - Choix des variétés
  - Optimisation des rotations
  - Amélioration des pratiques
  - Prévention des problèmes

### 6.2 Capteurs IoT
- **Monitoring automatique**:
  - Humidité du sol
  - Température ambiante
  - Luminosité
  - pH du sol

- **Alertes contextuelles**:
  - Irrigation nécessaire
  - Conditions de stress
  - Moment optimal pour récolte
  - Risques climatiques

### 6.3 Communauté et partage
- **Échange d'expériences**:
  - Comparaison avec autres jardiniers
  - Partage de techniques
  - Retours d'expérience
  - Conseils localisés

- **Marketplace intégrée**:
  - Échange de graines
  - Vente de surplus
  - Partage d'outils
  - Services de jardinage

## 7. Métriques et KPIs

### 7.1 Adoption et engagement
- **Utilisation de la planification**:
  - Nombre de cultures planifiées
  - Taux de suivi des recommandations
  - Fréquence de mise à jour
  - Satisfaction des prédictions

### 7.2 Performance des cultures
- **Précision des prédictions**:
  - Écart dates prévues/réelles
  - Précision des rendements
  - Taux de réussite des cultures
  - Amélioration des pratiques

### 7.3 Valeur ajoutée
- **Impact sur les utilisateurs**:
  - Augmentation des rendements
  - Réduction des pertes
  - Amélioration de la qualité
  - Économies réalisées

## 8. Roadmap d'implémentation

### 8.1 Phase 1 (6 semaines) - Base
- **Semaine 1-2**: Modèle de données et catalogue
- **Semaine 3-4**: Planification et calendrier
- **Semaine 5-6**: Interface utilisateur de base

### 8.2 Phase 2 (6 semaines) - Suivi
- **Semaine 7-8**: Suivi des cultures et statuts
- **Semaine 9-10**: Gestion des récoltes
- **Semaine 11-12**: Analyses et statistiques

### 8.3 Phase 3 (4 semaines) - Avancé
- **Semaine 13-14**: Intégration météo et prédictions
- **Semaine 15-16**: Optimisation et IA

## 9. Considérations spéciales

### 9.1 Localisation
- **Adaptation géographique**:
  - Zones climatiques
  - Variétés locales
  - Pratiques régionales
  - Réglementations locales

### 9.2 Saisonnalité
- **Gestion des cycles**:
  - Cultures d'hiver/été
  - Rotations pluriannuelles
  - Conservation des données
  - Planification long terme

### 9.3 Évolutivité
- **Croissance des besoins**:
  - Nouveaux types de cultures
  - Techniques innovantes
  - Intégrations additionnelles
  - Scaling international