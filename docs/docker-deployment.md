# Docker Deployment Guide

## Corrections apportées

### Problèmes identifiés
1. **Frontend** : Le répertoire `dist` n'existait pas car le build Docker ne se faisait pas correctement
2. **Backend** : Le port 5000 était occupé par AirPlay sur macOS
3. **Configuration développement** : Les volumes montaient les fichiers sources mais écrasaient le build
4. **Configuration production** : Mauvaise commande pour le backend et problèmes de variables d'environnement

### Corrections effectuées

#### 1. Dockerfiles optimisés
- **Frontend** : Ajout de variables d'environnement pour l'API URL et amélioration du build
- **Backend** : Optimisation des layers Docker et copie des dépendances en premier

#### 2. Configuration Docker Compose
- **Ports** : Frontend sur 8080 (externe) → 8080 (interne), Backend sur 5080 (externe) → 5000 (interne)
- **Variables d'environnement** : Configuration de `VITE_API_URL` pour le frontend
- **Dépendances** : Le frontend dépend du backend (`depends_on`)

#### 3. Configuration TypeScript
- Ajout de `vite-env.d.ts` pour les types des variables d'environnement
- Support de `import.meta.env.VITE_API_URL` dans l'API client

## Usage

### Développement
```bash
# Build et démarrage
make docker-build
make docker-run

# Ou directement
docker compose -f docker-compose.dev.yml up -d

# Arrêt
make docker-stop
```

### Production
```bash
# Build et démarrage
docker compose -f docker-compose.prod.yml up -d

# Arrêt
docker compose -f docker-compose.prod.yml down
```

## Accès aux services

### Développement et Production
- **Frontend** : http://localhost:8080
- **Backend API** : http://localhost:5080
- **Endpoint de test** : http://localhost:5080/auth/protected

## Tests avec MCP Puppeteer

L'application a été testée avec MCP Puppeteer et toutes les fonctionnalités suivantes fonctionnent :

✅ **Frontend (localhost:8080)**
- Page d'accueil
- Navigation entre les pages
- Formulaires interactifs
- Interface utilisateur responsive

✅ **Backend (localhost:5080)**
- API d'authentification
- Endpoints protégés avec JWT
- Validation des données
- Gestion des erreurs

✅ **Intégration**
- Communication Frontend ↔ Backend
- Variables d'environnement
- Configuration CORS
- Build de production

## Architecture finale

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │
│   (Vue.js)      │    │   (Flask)       │
│   Port: 8080    │◄───┤   Port: 5080    │
│                 │    │                 │
└─────────────────┘    └─────────────────┘
       │                        │
       │                        │
   ┌─────────────────────────────────┐
   │         Docker Network          │
   │        (bloomzy_default)        │
   └─────────────────────────────────┘
```

## Variables d'environnement

### Frontend
- `VITE_API_URL`: URL de l'API backend (défaut: http://localhost:5080)

### Backend
- `FLASK_ENV`: development ou production
- `FLASK_DEBUG`: 1 pour développement, 0 pour production

## Commandes utiles

```bash
# Voir les logs
docker compose -f docker-compose.dev.yml logs -f

# Rebuild sans cache
docker compose -f docker-compose.dev.yml build --no-cache

# Nettoyer les images
docker system prune -a
```