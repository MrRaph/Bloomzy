<template>
  <div>
    <BaseForm
      title="🌱 Inscription"
      description="Créez votre compte Bloomzy"
      :fields="signupFields"
      :initial-values="{ email: '', username: '', password: '', confirmPassword: '' }"
      :validate="validateForm"
      :on-submit="handleSignup"
      :loading="authStore.isLoading"
      loading-text="Création du compte..."
      :general-error="authStore.error"
    >
      <template #submit-label>Créer mon compte</template>
      <template #footer>
        <p>
          Déjà un compte ?
          <router-link to="/login" class="link">Se connecter</router-link>
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

const signupFields = [
  {
    name: 'email',
    label: 'Email',
    type: 'email',
    required: true,
    placeholder: 'votre@email.com',
    autocomplete: 'email'
  },
  {
    name: 'username',
    label: 'Nom d\'utilisateur',
    type: 'text',
    required: true,
    placeholder: 'Votre nom d\'utilisateur',
    autocomplete: 'username'
  },
  {
    name: 'password',
    label: 'Mot de passe',
    type: 'password',
    required: true,
    placeholder: 'Minimum 8 caractères',
    autocomplete: 'new-password',
    hint: 'Le mot de passe doit contenir au moins 8 caractères avec des lettres et des chiffres'
  },
  {
    name: 'confirmPassword',
    label: 'Confirmer le mot de passe',
    type: 'password',
    required: true,
    placeholder: 'Répétez votre mot de passe',
    autocomplete: 'new-password'
  }
]

const validateForm = (values: Record<string, any>) => {
  const errors: Record<string, string> = {}
  
  if (values.password && values.password.length < 8) {
    errors.password = 'Le mot de passe doit contenir au moins 8 caractères'
  }
  
  if (values.password && values.confirmPassword && values.password !== values.confirmPassword) {
    errors.confirmPassword = 'Les mots de passe ne correspondent pas'
  }
  
  return errors
}

const handleSignup = async (formData: Record<string, any>) => {
  const success = await authStore.signup({
    email: formData.email,
    username: formData.username,
    password: formData.password
  })
  
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