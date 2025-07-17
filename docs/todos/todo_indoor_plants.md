# TODO Gestion Plantes d’Intérieur

## Objectif
Permettre la gestion intelligente des plantes d’intérieur avec notifications et journal de croissance.

### Étapes
1. **Catalogue des espèces** ([Issue #6](https://github.com/MrRaph/Bloomzy/issues/6))
   - Créer la branche `feature/indoor-catalog`.
   - Objectif : Modèle DB, endpoints REST, recherche/filtres.
   - Validation : Tests unitaires sur la recherche et l’ajout.

2. **Gestion des plantes utilisateur** ([Issue #7](https://github.com/MrRaph/Bloomzy/issues/7))
   - CRUD plantes, photos, localisation, santé.
   - Objectif : API REST, validation, synchronisation avec notifications.
   - Validation : Tests d’intégration, documentation API.

3. **Algorithme d’arrosage intelligent** ([Issue #8](https://github.com/MrRaph/Bloomzy/issues/8))
   - Calcul dynamique, intégration météo, historique.
   - Objectif : Implémentation, tests unitaires, documentation.
   - Validation : Précision validée par tests et feedback utilisateur.

4. **Journal de croissance** ([Issue #9](https://github.com/MrRaph/Bloomzy/issues/9))
   - Suivi photo, métriques, analyse IA.
   - Objectif : API, interface, tests unitaires.
   - Validation : Export, visualisation, tests d’intégration.

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation API et utilisateur
- PRs avec revue et merge
