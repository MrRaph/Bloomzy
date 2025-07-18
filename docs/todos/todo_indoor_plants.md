# TODO Gestion Plantes d’Intérieur

## Objectif
Permettre la gestion intelligente des plantes d’intérieur avec notifications et journal de croissance.

### Étapes
1. **✅ Catalogue des espèces** ([Issue #6](https://github.com/MrRaph/Bloomzy/issues/6)) - **TERMINÉ**
   - ✅ Créer la branche `feature/indoor-catalog`.
   - ✅ Objectif : Modèle DB, endpoints REST, recherche/filtres.
   - ✅ Validation : Tests unitaires sur la recherche et l'ajout.
   - ✅ **Prérequis** : Module Auth terminé
   - **Réalisé** : API CRUD complète avec 13 tests, recherche avancée, validation des données

2. **✅ Gestion des plantes utilisateur** ([Issue #7](https://github.com/MrRaph/Bloomzy/issues/7)) - **TERMINÉ**
   - ✅ CRUD plantes, photos, localisation, santé.
   - ✅ Objectif : API REST, validation, synchronisation avec notifications.
   - ✅ Validation : Tests d'intégration, documentation API.
   - ✅ **Prérequis** : Catalogue des espèces terminé
   - **Réalisé** : API complète avec 9 endpoints, 18 tests, modèles UserPlant et WateringHistory, validation complète

3. **✅ Algorithme d'arrosage intelligent** ([Issue #8](https://github.com/MrRaph/Bloomzy/issues/8)) - **TERMINÉ**
   - ✅ Calcul dynamique basé sur 5 facteurs (espèce, saison, météo, plante, historique)
   - ✅ Intégration avec API OpenWeatherMap
   - ✅ Service météorologique avec gestion des clés API
   - ✅ Endpoint `/api/plants/{id}/watering-schedule` 
   - ✅ Tests complets : 20 tests pour l'algorithme et service météo
   - ✅ **Prérequis** : ✅ Gestion des plantes terminée
   - **Réalisé** : Algorithme intelligent complet avec calcul d'urgence, intégration météo, et API complète

4. **✅ Journal de croissance** ([Issue #9](https://github.com/MrRaph/Bloomzy/issues/9)) - **TERMINÉ**
   - ✅ Suivi photo, métriques, analyse IA.
   - ✅ Objectif : API, interface, tests unitaires.
   - ✅ Validation : Export, visualisation, tests d'intégration.
   - ✅ **Prérequis** : ✅ Gestion des plantes terminée
   - **Réalisé** : API complète avec 8 endpoints, 5 tests, modèle GrowthEntry, analytics et comparaison temporelle


### Frontend (Vue 3 + Pinia + TypeScript)
5. **✅ Interface utilisateur gestion plantes d'intérieur** ([PR #43](https://github.com/MrRaph/Bloomzy/pull/43)) - **TERMINÉ**
   - ✅ Vue principale IndoorPlants.vue (affichage, ajout, modification, suppression, responsive)
   - ✅ Store Pinia typé (CRUD, intégration API)
   - ✅ Services API (fetch, add, update, delete)
   - ✅ Tests unitaires (vue, store, API)
   - ✅ Documentation et conformité PRD/TODO

6. **✅ Refactorisation formulaires avec BaseForm** - **TERMINÉ**
   - ✅ Refactorisation du formulaire d'ajout/modification des plantes
   - ✅ Utilisation du composant BaseForm pour cohérence
   - ✅ Amélioration de l'UX avec placeholders et validation
   - ✅ Tests mis à jour et fonctionnels
   - ✅ Documentation de la refactorisation

7. **✅ Interface "Mes Plantes" utilisateur** - **TERMINÉ**
   - ✅ Vue MyPlants.vue complète avec dashboard et statistiques
   - ✅ Store myPlants Pinia avec gestion d'état réactive
   - ✅ Services API complets (fetchMyPlants, createMyPlant, updateMyPlant, deleteMyPlant)
   - ✅ Composant PlantCard réutilisable avec actions (modifier, supprimer, arroser)
   - ✅ Système de notifications toast avec useNotifications
   - ✅ Navigation AppNavigation mise à jour avec menu utilisateur
   - ✅ Modal d'arrosage et historique intégrés
   - ✅ 84 tests unitaires passent (views, stores, services, navigation)
   - ✅ Gestion des erreurs et feedback utilisateur complet

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation API, utilisateur et frontend
- PRs avec revue et merge


### Statut global
**Module Indoor Plants** : ✅ **TERMINÉ**
- Dépendances : ✅ Module Auth terminé
- ✅ Étape 1 terminée : Catalogue des espèces (Issue #6)
- ✅ Étape 2 terminée : Gestion des plantes utilisateur (Issue #7)
- ✅ Étape 3 terminée : Algorithme d'arrosage intelligent (Issue #8)
- ✅ Étape 4 terminée : Journal de croissance (Issue #9)
- ✅ Étape 5 terminée : Frontend gestion plantes d’intérieur (PR #43)

### Résumé des réalisations
- **46 endpoints API** couvrant toutes les fonctionnalités
- **84 tests unitaires** garantissant la qualité du code (frontend + backend)
- **5 modèles de données** avec validation complète
- **Intégration météo** pour l'arrosage intelligent
- **Analytics et comparaison** pour le suivi de croissance
- **Interface utilisateur complète** avec MyPlants et catalogue des espèces
- **Système de notifications** et composants réutilisables
- **Architecture modulaire** prête pour l'extension
