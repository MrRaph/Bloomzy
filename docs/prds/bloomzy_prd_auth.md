# GrowWise - PRD Authentification et Gestion Utilisateurs

## 1. Objectifs

### Objectif principal
Créer un système d'authentification sécurisé et une gestion utilisateur complète permettant une expérience personnalisée et la protection des données.

### Objectifs secondaires
- Onboarding fluide pour nouveaux utilisateurs
- Gestion sécurisée des clés API personnelles
- Profils utilisateur riches et personnalisables
- Système de préférences avancé

## 2. Fonctionnalités

### 2.1 Authentification

#### 2.1.1 Inscription
- **Méthodes supportées**:
  - Email/mot de passe
  - Google OAuth
  - Apple Sign-In (pour iOS)
  - Inscription invité (limitation des fonctionnalités)

- **Validation**:
  - Vérification email obligatoire
  - Politique de mot de passe forte
  - Protection contre les bots (reCAPTCHA)
  - Limite de tentatives d'inscription

#### 2.1.2 Connexion
- **Authentification multi-facteurs optionnelle**:
  - SMS
  - Application d'authentification (TOTP)
  - Email de confirmation

- **Gestion de session**:
  - Tokens JWT avec refresh token
  - Expiration configurée (24h par défaut)
  - Possibilité de "Se souvenir de moi"
  - Déconnexion sur tous les appareils

### 2.2 Gestion du profil utilisateur

#### 2.2.1 Informations personnelles
- **Données obligatoires**:
  - Nom d'utilisateur unique
  - Email
  - Localisation (ville/région pour météo)

- **Données optionnelles**:
  - Nom complet
  - Photo de profil
  - Bio/description
  - Niveau d'expérience en jardinage
  - Spécialités (légumes, fleurs, plantes d'intérieur)

#### 2.2.2 Préférences
- **Jardinage**:
  - Type de climat/zone de rusticité
  - Préférences de culture (bio, permaculture, etc.)
  - Espace disponible (balcon, petit jardin, grande parcelle)
  - Plantes préférées

- **Notifications**:
  - Fréquence des rappels
  - Horaires préférés
  - Canaux (push, email, SMS)
  - Types de notifications activées

### 2.3 Gestion des clés API

#### 2.3.1 Configuration IA
- **Stockage sécurisé**:
  - Chiffrement AES-256
  - Clés stockées séparément des données utilisateur
  - Validation au moment de la sauvegarde

- **Providers supportés**:
  - OpenAI (ChatGPT)
  - Anthropic (Claude)
  - Possibilité d'extension future

- **Gestion**:
  - Test de connexion lors de l'ajout
  - Monitoring d'usage avec alertes
  - Rotation automatique optionnelle

### 2.4 Paramètres de compte

#### 2.4.1 Sécurité
- **Gestion des mots de passe**:
  - Changement de mot de passe
  - Historique des mots de passe (éviter la réutilisation)
  - Réinitialisation sécurisée

- **Sessions actives**:
  - Visualisation des sessions
  - Géolocalisation des connexions
  - Révocation sélective ou globale

#### 2.4.2 Confidentialité
- **Contrôle de visibilité**:
  - Profil public/privé
  - Partage des statistiques
  - Participation aux fonctionnalités communautaires

- **Données personnelles**:
  - Export des données (RGPD)
  - Suppression de compte
  - Gestion des consentements

## 3. Spécifications techniques

### 3.1 Base de données

#### 3.1.1 Modèle utilisateur
```sql
users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP
);

user_profiles (
    user_id UUID REFERENCES users(id),
    full_name VARCHAR(100),
    bio TEXT,
    profile_picture_url VARCHAR(500),
    location VARCHAR(100),
    experience_level VARCHAR(20),
    specialties TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

user_preferences (
    user_id UUID REFERENCES users(id),
    climate_zone VARCHAR(10),
    garden_type VARCHAR(50),
    notification_frequency VARCHAR(20),
    notification_channels JSONB,
    preferred_units VARCHAR(10),
    timezone VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### 3.1.2 Clés API
```sql
user_api_keys (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,
    encrypted_key TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3.2 API Endpoints

#### 3.2.1 Authentification
```
POST /api/auth/register
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
POST /api/auth/verify-email
POST /api/auth/reset-password
POST /api/auth/change-password
```

#### 3.2.2 Profil utilisateur
```
GET /api/users/profile
PUT /api/users/profile
DELETE /api/users/account
GET /api/users/preferences
PUT /api/users/preferences
```

#### 3.2.3 Clés API
```
POST /api/users/api-keys
GET /api/users/api-keys
PUT /api/users/api-keys/{id}
DELETE /api/users/api-keys/{id}
POST /api/users/api-keys/{id}/test
```

### 3.3 Sécurité

#### 3.3.1 Authentification
- **JWT avec RS256**
- **Refresh token rotation**
- **Rate limiting par IP et par utilisateur**
- **Blacklist des tokens révoqués**

#### 3.3.2 Protection des données
- **Chiffrement des clés API avec Fernet**
- **Hashage des mots de passe avec bcrypt**
- **Validation stricte des entrées**
- **Audit trail des actions sensibles**

## 4. Expérience utilisateur

### 4.1 Onboarding

#### 4.1.1 Étapes
1. **Inscription** (email ou OAuth)
2. **Vérification email**
3. **Configuration du profil**
4. **Préférences de base**
5. **Configuration optionnelle de l'IA**
6. **Tutoriel guidé**

#### 4.1.2 Interface
- **Progressive disclosure**
- **Possibilité de passer les étapes**
- **Barre de progression**
- **Aide contextuelle**

### 4.2 Gestion du profil

#### 4.2.1 Dashboard utilisateur
- **Aperçu des informations**
- **Statistiques d'utilisation**
- **Statut des clés API**
- **Activité récente**

#### 4.2.2 Paramètres
- **Organisation par catégories**
- **Recherche dans les paramètres**
- **Prévisualisation des changements**
- **Confirmation pour actions critiques**

## 5. Tests et validation

### 5.1 Tests unitaires
- **Authentification et autorisation**
- **Validation des données**
- **Chiffrement/déchiffrement**
- **Gestion des erreurs**

### 5.2 Tests d'intégration
- **Flux d'inscription complet**
- **Connexion avec OAuth**
- **Gestion des sessions**
- **APIs externes**

### 5.3 Tests de sécurité
- **Injection SQL**
- **Attaques par force brute**
- **Validation des tokens**
- **Gestion des permissions**

## 6. Métriques

### 6.1 Inscription
- **Taux de conversion inscription**
- **Temps de complétion onboarding**
- **Méthodes d'inscription préférées**
- **Taux d'abandon par étape**

### 6.2 Engagement
- **Taux de connexion régulière**
- **Temps entre connexions**
- **Utilisation des fonctionnalités**
- **Taux de rétention**

### 6.3 Sécurité
- **Tentatives d'intrusion**
- **Comptes compromis**
- **Utilisation 2FA**
- **Rotation des clés API**

## 7. Déploiement

### 7.1 Configuration
- **Variables d'environnement**
- **Secrets management**
- **Configuration base de données**
- **Certificats SSL**

### 7.2 Monitoring
- **Logs d'authentification**
- **Métriques de performance**
- **Alertes sécurité**
- **Health checks**

### 7.3 Scalabilité
- **Cache Redis pour sessions**
- **Load balancing**
- **Réplication base de données**
- **CDN pour avatars**