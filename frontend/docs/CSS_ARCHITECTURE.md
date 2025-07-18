# Architecture CSS - Frontend Bloomzy

## Structure des styles

Le projet utilise une architecture CSS modulaire et maintenable :

```
frontend/src/styles/
├── main.css              # Point d'entrée principal
├── variables.css          # Variables CSS globales
├── buttons.css           # Styles des boutons réutilisables
└── components/
    └── base-form.css     # Styles spécifiques au composant BaseForm
```

## Principes d'organisation

### 1. Variables CSS globales (`variables.css`)
- Centralise toutes les valeurs de design (couleurs, espacements, tailles)
- Utilise les custom properties CSS (`--variable-name`)
- Facilite la maintenance et la cohérence visuelle

### 2. Styles de composants communs (`buttons.css`)
- Contient les styles réutilisables (boutons, liens, etc.)
- Classes utilitaires utilisables dans toute l'application

### 3. Styles de composants spécifiques (`components/`)
- Un fichier CSS par composant Vue
- Utilise les variables globales pour la cohérence
- Maintient l'encapsulation des styles

## Utilisation

### Dans un composant Vue
```vue
<style scoped>
@import '../styles/components/nom-composant.css';
</style>
```

### Variables disponibles
```css
/* Couleurs */
--color-primary: #059669;
--color-primary-dark: #047857;
--color-text-primary: #374151;

/* Espacements */
--spacing-sm: 0.5rem;
--spacing-md: 0.75rem;
--spacing-lg: 1rem;

/* Et bien d'autres... */
```

## Avantages

1. **Maintenabilité** : Changement centralisé des variables
2. **Réutilisabilité** : Styles partagés entre composants
3. **Cohérence** : Design system unifié
4. **Performance** : CSS optimisé et modulaire
5. **Lisibilité** : Séparation claire entre logique et présentation

## Bonnes pratiques

- Toujours utiliser les variables CSS au lieu de valeurs hardcodées
- Un fichier CSS par composant dans `components/`
- Préfixer les classes spécifiques au composant
- Documenter les nouvelles variables ajoutées
- Maintenir la hiérarchie d'import dans `main.css`
