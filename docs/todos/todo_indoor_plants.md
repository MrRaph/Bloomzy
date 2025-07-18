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

2. **🔄 Gestion des plantes utilisateur** ([Issue #7](https://github.com/MrRaph/Bloomzy/issues/7)) - **PRÊT À COMMENCER**
   - CRUD plantes, photos, localisation, santé.
   - Objectif : API REST, validation, synchronisation avec notifications.
   - Validation : Tests d'intégration, documentation API.
   - **Prérequis** : ✅ Catalogue des espèces terminé

3. **🔄 Algorithme d'arrosage intelligent** ([Issue #8](https://github.com/MrRaph/Bloomzy/issues/8)) - **EN ATTENTE**
   - Calcul dynamique, intégration météo, historique.
   - Objectif : Implémentation, tests unitaires, documentation.
   - Validation : Précision validée par tests et feedback utilisateur.
   - **Prérequis** : Gestion des plantes terminée

4. **🔄 Journal de croissance** ([Issue #9](https://github.com/MrRaph/Bloomzy/issues/9)) - **EN ATTENTE**
   - Suivi photo, métriques, analyse IA.
   - Objectif : API, interface, tests unitaires.
   - Validation : Export, visualisation, tests d'intégration.
   - **Prérequis** : Gestion des plantes terminée

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation API et utilisateur
- PRs avec revue et merge

### Statut global
**Module Indoor Plants** : 🔄 **EN COURS**
- Dépendances : ✅ Module Auth terminé
- ✅ Étape 1 terminée : Catalogue des espèces (Issue #6)
- 🔄 Prochaine étape : Gestion des plantes utilisateur (Issue #7)
