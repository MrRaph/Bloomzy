# Documentation API Backend Bloomzy

## Vue d'ensemble

Cette documentation couvre toutes les APIs du backend Bloomzy, organisées par modules fonctionnels.

## 📚 Index de la Documentation

### 🔐 Authentification
- **[API d'Authentification](auth_api.md)** - Signup, Login, JWT
- **[API Clés API](api_keys_api.md)** - Gestion des clés API IA

### 🌱 Plantes d'Intérieur
- **[API Plantes d'Intérieur](indoor_plants_api.md)** - Vue d'ensemble et catalogue des espèces
- **[API Plantes Utilisateur](user_plants_api.md)** - Gestion des plantes personnelles et arrosage

### 🔧 Outils et Infrastructure
- **[Makefile](makefile.md)** - Commandes d'automatisation
- **[Dockerfile](dockerfile.md)** - Containerisation
- **[Meilleures Pratiques](best_practices.md)** - Guidelines de développement

## 🏗️ Architecture des APIs

### Modules Complétés ✅

#### 1. Module Authentification
- **Statut** : ✅ Terminé
- **Issues** : #1-#4
- **Tests** : 37 tests passants
- **Endpoints** : 
  - Signup/Login avec JWT
  - Gestion des profils utilisateur
  - Gestion des clés API IA

#### 2. Module Plantes d'Intérieur (Partiel)
- **Statut** : 🔄 En cours (2/4 terminées)
- **Issues** : #6-#9
- **Tests** : 31 tests passants

**✅ Catalogue des Espèces (Issue #6)**
- Endpoints CRUD pour les espèces de plantes
- Recherche et filtrage
- 13 tests passants

**✅ Plantes Utilisateur (Issue #7)**
- Gestion CRUD des plantes personnelles
- Upload de photos
- Historique d'arrosage
- Authentification JWT
- 18 tests passants

### Modules En Cours 🔄

#### 3. Module Plantes d'Intérieur (Suite)
**🔄 Algorithme d'Arrosage (Issue #8)** - Prêt à commencer
- Calcul intelligent des besoins d'arrosage
- Intégration météo
- Notifications automatiques

**🔄 Journal de Croissance (Issue #9)** - Prêt à commencer
- Suivi photographique
- Métriques de croissance
- Analyse IA

## 📊 Statistiques Globales

### Tests
- **Total** : 68 tests passants (100%)
- **Couverture** : Modules Auth et Indoor Plants (partiel)
- **Méthodologie** : TDD stricte

### Sécurité
- **Authentification** : JWT avec expiration
- **Validation** : Validation complète des données
- **Isolation** : Séparation stricte des données utilisateur
- **Chiffrement** : Données sensibles chiffrées

### Documentation
- **API** : Complète pour tous les modules terminés
- **Tests** : Documentation inline
- **Exemples** : Curl commands pour tous les endpoints

## 🚀 Démarrage Rapide

### Prérequis
```bash
cd backend
make venv  # Créer l'environnement virtuel
```

### Lancement
```bash
flask run  # Démarrer le serveur de développement
```

### Tests
```bash
make test  # Exécuter tous les tests
```

### Endpoints Principaux

**Authentification**
- `POST /auth/signup` - Créer un compte
- `POST /auth/login` - Se connecter
- `GET /auth/profile` - Profil utilisateur

**Plantes d'Intérieur**
- `GET /indoor-plants/` - Catalogue des espèces
- `GET /api/plants/my-plants` - Mes plantes
- `POST /api/plants/my-plants` - Ajouter une plante
- `POST /api/plants/watering` - Enregistrer un arrosage

## 🔗 Liens Utiles

- **Code Source** : `/backend/routes/`, `/backend/models/`
- **Tests** : `/backend/tests/`
- **Configuration** : `/backend/Makefile`
- **TODOs** : `/docs/todos/`

## 📋 Prochaines Étapes

1. **Algorithme d'Arrosage Intelligent** (Issue #8)
2. **Journal de Croissance** (Issue #9)
3. **Module Architecture** (Issues #26-#29)
4. **Modules Métier** (Garden, Notifications, AI, Community)

---

**Dernière mise à jour** : 18 juillet 2025  
**Version** : Phase 2 en cours  
**Statut** : 🔄 Développement actif