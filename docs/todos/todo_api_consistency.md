# TODO : Cohérence API Backend/Frontend

## Objectif
Assurer la cohérence complète entre les routes backend disponibles et leur utilisation dans le frontend, implémenter les fonctionnalités manquantes et corriger les incohérences.

## Priorité : HAUTE

## Issues à résoudre

### 1. Route manquante dans le backend
- [ ] **POST /auth/refresh** : Implémentée dans le frontend mais absente du backend
  - Créer l'endpoint dans `backend/routes/auth.py`
  - Implémenter la logique de refresh token avec JWT
  - Tester l'endpoint avec le frontend

### 2. Module API Keys non intégré au frontend
- [ ] Créer les services frontend pour les API Keys
  - Ajouter les fonctions dans `frontend/src/services/api.ts`
  - Créer les types TypeScript dans `frontend/src/types/`
- [ ] Créer le store Pinia pour les API Keys
  - `frontend/src/stores/apiKeys.ts`
  - Gestion d'état pour CRUD des clés API
- [ ] Créer les composants UI
  - Vue de gestion des clés API
  - Formulaire d'ajout/modification de clé
  - Interface de test des clés
- [ ] Ajouter les routes Vue.js
  - `/settings/api-keys` pour la gestion des clés
  - Intégrer dans la navigation

### 3. Module Growth Journal non intégré au frontend
- [ ] Créer les services frontend pour le journal de croissance
  - Ajouter les fonctions dans `frontend/src/services/api.ts`
  - Créer les types TypeScript dans `frontend/src/types/`
- [ ] Créer le store Pinia pour le journal de croissance
  - `frontend/src/stores/growthJournal.ts`
  - Gestion des entrées, analytics, comparaisons
- [ ] Créer les composants UI
  - Vue du journal de croissance par plante
  - Formulaire d'ajout d'entrée
  - Graphiques de croissance et analytics
  - Comparaison de périodes
  - Upload de photos de croissance
- [ ] Ajouter les routes Vue.js
  - `/plants/:id/journal` pour le journal d'une plante
  - `/plants/:id/analytics` pour les analyses
  - Intégrer dans la navigation des plantes

### 4. Routes backend sous-utilisées
- [ ] **GET /indoor-plants/<id>** : Implémenter dans le frontend
  - Ajouter la fonction dans `frontend/src/services/api.ts`
  - Utiliser pour afficher les détails d'une espèce
  - Créer une vue de détail d'espèce
- [ ] **GET /api/plants/my-plants/<id>** : Implémenter dans le frontend
  - Ajouter la fonction dans `frontend/src/services/api.ts`
  - Utiliser pour la vue détaillée d'une plante personnelle
  - Améliorer la navigation entre liste et détail
- [ ] **PUT /api/plants/watering/<id>** : Implémenter dans le frontend
  - Ajouter la fonction dans `frontend/src/services/api.ts`
  - Permettre la modification d'un enregistrement d'arrosage
  - Ajouter l'interface de modification dans l'historique

### 5. Routes techniques à évaluer
- [ ] **GET /auth/protected** : Évaluer l'utilité
  - Route de test d'authentification
  - Décider si elle doit être utilisée ou supprimée
- [ ] **OPTIONS /indoor-plants/<id>** : Route CORS automatique
  - Pas d'action nécessaire (gérée automatiquement)

## Plan d'implémentation

### Phase 1 : Corrections critiques (Semaine 1)
1. Implémenter `POST /auth/refresh` dans le backend
2. Ajouter `GET /indoor-plants/<id>` au frontend
3. Ajouter `GET /api/plants/my-plants/<id>` au frontend
4. Tests d'intégration pour ces corrections

### Phase 2 : Module API Keys (Semaine 2)
1. Services et types frontend
2. Store Pinia
3. Composants UI basiques
4. Routes et navigation
5. Tests unitaires et d'intégration

### Phase 3 : Module Growth Journal (Semaines 3-4)
1. Services et types frontend
2. Store Pinia avec analytics
3. Composants UI avancés (graphiques, comparaisons)
4. Routes et navigation
5. Tests unitaires et d'intégration

### Phase 4 : Améliorations UX (Semaine 5)
1. Implémenter `PUT /api/plants/watering/<id>`
2. Améliorer les vues de détails
3. Optimisations et polish
4. Tests end-to-end complets

## Critères de validation

### Pour chaque fonctionnalité :
- [ ] Route backend accessible et fonctionnelle
- [ ] Service frontend correspondant implémenté
- [ ] Store Pinia avec gestion d'état appropriée
- [ ] Interface utilisateur intuitive et responsive
- [ ] Tests unitaires avec couverture > 80%
- [ ] Tests d'intégration backend/frontend
- [ ] Documentation utilisateur mise à jour

### Tests de cohérence globale :
- [ ] Audit complet backend/frontend sans routes orphelines
- [ ] Tests end-to-end sur tous les parcours utilisateur
- [ ] Performance acceptable sur toutes les opérations
- [ ] Gestion d'erreur cohérente sur toutes les routes

## Ressources nécessaires

### Développement :
- Types TypeScript pour nouveaux modules
- Composants Vue.js avec composition API
- Graphiques pour les analytics (Chart.js/D3.js)
- Tests avec Vitest et Vue Test Utils

### Documentation :
- Mise à jour des PRDs concernés
- Documentation API complète
- Guide utilisateur pour nouvelles fonctionnalités

## Estimation

**Effort total :** 4-5 semaines développeur
**Complexité :** Moyenne à élevée (analytics et graphiques)
**Risques :** Intégration des graphiques, performance des analytics

## Notes

- Priorité sur les corrections critiques (Phase 1) avant nouvelles fonctionnalités
- Le module Growth Journal est le plus complexe (analytics, graphiques)
- Considérer l'utilisation d'une librairie de graphiques mature
- Prévoir des tests de performance pour les analytics de croissance
- S'assurer de la cohérence UX avec l'existant

## Suivi

- [ ] Issue GitHub créée avec ce TODO
- [ ] Planning détaillé défini par phase
- [ ] Assignation des développeurs
- [ ] Revues de code planifiées par phase
- [ ] Tests d'acceptance définis

---

**Prochaine étape :** Créer les issues GitHub correspondantes et commencer par la Phase 1.
