# Contraintes Frontend

## Gestion des plantes d’intérieur (Indoor Plants)

### Vue principale
- `src/views/IndoorPlants.vue` :
  - Affichage de la liste des plantes d’intérieur de l’utilisateur
  - Ajout, modification, suppression de plante (formulaire intégré)
  - Responsive et accessible

### Store Pinia
- `src/stores/indoorPlants.ts` :
  - Gestion de l’état des plantes (CRUD)
  - Typage strict avec interface IndoorPlant
  - Intégration directe avec les services API

### Services API
- `src/services/api.ts` :
  - Fonctions fetchIndoorPlants, createIndoorPlant, updateIndoorPlant, deleteIndoorPlant
  - Utilisation d’Axios avec intercepteurs JWT

### Tests unitaires
- `src/views/IndoorPlants.spec.ts` : tests de la vue (affichage, formulaire, interaction store)
- `src/stores/indoorPlants.spec.ts` : tests du store (CRUD, intégration API)
- `src/services/indoorPlants.spec.ts` : tests des fonctions API (mock axios)

### Validation
- Couverture complète par tests unitaires (Vitest)
- PR #43, conforme PRD et TODOs

### Lien de la PR
- https://github.com/MrRaph/Bloomzy/pull/43
- Framework : Vue.js 3 (Composition API)
- Build tool : Vite
- UI : Tailwind CSS
- State management : Pinia
- PWA : Workbox
- Tests : Vitest + Cypress
- Structure recommandée :
  - frontend/src
  - frontend/tests
  - frontend/package.json
- Respecter la factorisation et la non-répétition
- Documentation à jour à chaque ajout/modification
- Respect du Git Flow (branche, PR, merge sur main après validation)
