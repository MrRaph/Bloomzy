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

4. **🔄 Journal de croissance** ([Issue #9](https://github.com/MrRaph/Bloomzy/issues/9)) - **PRÊT À COMMENCER**
   - Suivi photo, métriques, analyse IA.
   - Objectif : API, interface, tests unitaires.
   - Validation : Export, visualisation, tests d'intégration.
   - **Prérequis** : ✅ Gestion des plantes terminée

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation API et utilisateur
- PRs avec revue et merge

### Statut global
**Module Indoor Plants** : 🔄 **EN COURS**
- Dépendances : ✅ Module Auth terminé
- ✅ Étape 1 terminée : Catalogue des espèces (Issue #6)
- ✅ Étape 2 terminée : Gestion des plantes utilisateur (Issue #7)
- ✅ Étape 3 terminée : Algorithme d'arrosage intelligent (Issue #8)
- 🔄 Prochaine étape : Journal de croissance (Issue #9)
