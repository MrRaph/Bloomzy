# Bonnes pratiques TypeScript - Frontend

## Correction des erreurs courantes

### 1. Imports inutilisés
**Problème** : `'ref' is declared but its value is never read.`
**Solution** : Supprimer les imports non utilisés pour éviter les erreurs de compilation.

```typescript
// ❌ Mauvais
import { reactive, watch, ref, computed } from 'vue'

// ✅ Bon
import { reactive, watch, computed } from 'vue'
```

### 2. Typage strict pour les données de formulaire
**Problème** : `Record<string, any>` ne satisfait pas les types stricts
**Solution** : Créer des objets typés explicites avant les appels API.

```typescript
// ❌ Mauvais
function submitForm(formData: Record<string, any>) {
  store.addPlant(formData); // Erreur TS2345
}

// ✅ Bon
function submitForm(formData: Record<string, any>) {
  const plantData = {
    name: formData.name as string,
    species: formData.species as string
  };
  store.addPlant(plantData);
}
```

### 3. Gestion des types null/undefined
**Problème** : `string | null` n'est pas assignable à `string | undefined`
**Solution** : Utiliser l'opérateur `||` pour convertir `null` en `undefined`.

```typescript
// ❌ Mauvais
:general-error="authStore.error"

// ✅ Bon
:general-error="authStore.error || undefined"
```

### 4. Typage explicite des credentials
**Problème** : Passer `Record<string, any>` au lieu du type attendu
**Solution** : Créer un objet avec le type correct.

```typescript
// ❌ Mauvais
const handleLogin = async (formData: Record<string, any>) => {
  const success = await authStore.login(formData) // Erreur TS2345
}

// ✅ Bon
const handleLogin = async (formData: Record<string, any>) => {
  const credentials: LoginCredentials = {
    email: formData.email as string,
    password: formData.password as string
  }
  const success = await authStore.login(credentials)
}
```

## Règles générales

1. **Toujours typer les imports** : Importer les types nécessaires
2. **Éviter `any`** : Utiliser des types spécifiques quand possible
3. **Gérer null/undefined** : Utiliser `||` ou `??` pour les conversions
4. **Créer des objets typés** : Ne pas passer `Record<string, any>` directement
5. **Supprimer les imports inutiles** : Éviter les erreurs de compilation

## Commandes utiles

```bash
# Vérifier les erreurs TypeScript
npm run build

# Vérifier en mode développement
npm run dev
```

Ces corrections garantissent que le build Docker réussira sans erreurs TypeScript.