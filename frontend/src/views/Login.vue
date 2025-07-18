<template>
  <div v-if="authStore.isAuthReady">
    <BaseForm
      title="🌱 Connexion"
      description="Connectez-vous à votre compte Bloomzy"
      :fields="loginFields"
      :initial-values="{ email: '', password: '' }"
      :on-submit="handleLogin"
      :loading="authStore.isLoading"
      loading-text="Connexion..."
      :general-error="authStore.error"
    >
      <template #submit-label>Se connecter</template>
      <template #footer>
        <p>
          Pas encore de compte ?
          <router-link to="/signup" class="link">Créer un compte</router-link>
        </p>
      </template>
    </BaseForm>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseForm from '@/components/BaseForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const loginFields = [
  {
    name: 'email',
    label: 'Email',
    type: 'email',
    required: true,
    placeholder: 'votre@email.com',
    autocomplete: 'email'
  },
  {
    name: 'password',
    label: 'Mot de passe',
    type: 'password',
    required: true,
    placeholder: 'Votre mot de passe',
    autocomplete: 'current-password'
  }
]

const handleLogin = async (formData: Record<string, any>) => {
  const success = await authStore.login(formData)
  if (success) {
    router.push('/dashboard')
  }
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    router.push('/dashboard')
  }
})
</script>

<style scoped>
.link {
  color: #059669;
  text-decoration: none;
  font-weight: 600;
}

.link:hover {
  text-decoration: underline;
}

p {
  color: #6b7280;
  font-size: 0.9rem;
}
</style>