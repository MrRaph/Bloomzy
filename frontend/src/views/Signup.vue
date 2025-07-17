<template>
  <div class="signup-page">
    <div class="signup-container">
      <div class="signup-header">
        <h1>🌱 Inscription</h1>
        <p>Créez votre compte Bloomzy</p>
      </div>

      <form @submit.prevent="handleSignup" class="signup-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="votre@email.com"
            :disabled="authStore.isLoading"
          />
        </div>

        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="Votre nom d'utilisateur"
            :disabled="authStore.isLoading"
          />
        </div>

        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="Minimum 8 caractères"
            :disabled="authStore.isLoading"
          />
          <div class="password-hint">
            Le mot de passe doit contenir au moins 8 caractères avec des lettres et des chiffres
          </div>
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirmer le mot de passe</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            placeholder="Répétez votre mot de passe"
            :disabled="authStore.isLoading"
          />
        </div>

        <div class="error-message" v-if="authStore.error">
          {{ authStore.error }}
        </div>

        <div class="error-message" v-if="passwordError">
          {{ passwordError }}
        </div>

        <button type="submit" class="btn btn-primary" :disabled="authStore.isLoading || !isFormValid">
          <span v-if="authStore.isLoading">Création du compte...</span>
          <span v-else>Créer mon compte</span>
        </button>
      </form>

      <div class="signup-footer">
        <p>
          Déjà un compte ?
          <router-link to="/login" class="link">Se connecter</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  email: '',
  username: '',
  password: '',
  confirmPassword: ''
})

const passwordError = computed(() => {
  if (form.value.password && form.value.confirmPassword) {
    if (form.value.password !== form.value.confirmPassword) {
      return 'Les mots de passe ne correspondent pas'
    }
  }
  if (form.value.password && form.value.password.length < 8) {
    return 'Le mot de passe doit contenir au moins 8 caractères'
  }
  return null
})

const isFormValid = computed(() => {
  return form.value.email && 
         form.value.username && 
         form.value.password && 
         form.value.confirmPassword &&
         form.value.password === form.value.confirmPassword &&
         form.value.password.length >= 8
})

const handleSignup = async () => {
  if (!isFormValid.value) return

  const success = await authStore.signup({
    email: form.value.email,
    username: form.value.username,
    password: form.value.password
  })
  
  if (success) {
    router.push('/')
  }
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/')
  }
})
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
  padding: 2rem;
}

.signup-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
}

.signup-header {
  text-align: center;
  margin-bottom: 2rem;
}

.signup-header h1 {
  font-size: 2rem;
  color: #059669;
  margin-bottom: 0.5rem;
}

.signup-header p {
  color: #6b7280;
  font-size: 0.9rem;
}

.signup-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.form-group input {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

.form-group input:disabled {
  background-color: #f9fafb;
  cursor: not-allowed;
}

.password-hint {
  font-size: 0.8rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  text-align: center;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 1rem;
}

.btn-primary {
  background: #059669;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #047857;
  transform: translateY(-1px);
}

.btn-primary:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.signup-footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.signup-footer p {
  color: #6b7280;
  font-size: 0.9rem;
}

.link {
  color: #059669;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .signup-container {
    padding: 1.5rem;
  }
  
  .signup-header h1 {
    font-size: 1.5rem;
  }
}
</style>