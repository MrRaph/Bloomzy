# TODO Gestion Plantes d’Intérieur

## Objectif
Permettre la gestion intelligente des plantes d’intérieur avec notifications et journal de croissance.

### Étapes
1. **Catalogue des espèces**
   - Créer la branche `feature/indoor-catalog`.
   - Objectif : Modèle DB, endpoints REST, recherche/filtres.
   - Validation : Tests unitaires sur la recherche et l’ajout.

2. **Gestion des plantes utilisateur**
   - CRUD plantes, photos, localisation, santé.
   - Objectif : API REST, validation, synchronisation avec notifications.
   - Validation : Tests d’intégration, documentation API.

3. **Algorithme d’arrosage intelligent**
   - Calcul dynamique, intégration météo, historique.
   - Objectif : Implémentation, tests unitaires, documentation.
   - Validation : Précision validée par tests et feedback utilisateur.

4. **Journal de croissance**
   - Suivi photo, métriques, analyse IA.
   - Objectif : API, interface, tests unitaires.
   - Validation : Export, visualisation, tests d’intégration.

### Critères de validation
- Fonctionnalités testées (TDD)
- Documentation API et utilisateur
- PRs avec revue et merge
