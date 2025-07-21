<template>
  <div class="profile-page">
    <div class="profile-container">
      <div class="profile-header">
        <h1>👤 Mon profil</h1>
        <p>Gérez vos informations personnelles</p>
      </div>

      <div class="profile-content">
        <div class="profile-info" v-if="!isEditing">
          <div class="info-section">
            <h3>Informations générales</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>Email</label>
                <span>{{ authStore.user?.email }}</span>
              </div>
              <div class="info-item">
                <label>Nom d'utilisateur</label>
                <span>{{ authStore.user?.username }}</span>
              </div>
              <div class="info-item">
                <label>Biographie</label>
                <span>{{ authStore.user?.bio || 'Aucune biographie' }}</span>
              </div>
              <div class="info-item">
                <label>Localisation</label>
                <span>{{ authStore.user?.location || 'Non renseignée' }}</span>
              </div>
              <div class="info-item">
                <label>Langue</label>
                <span>{{ authStore.user?.language || 'fr' }}</span>
              </div>
              <div class="info-item">
                <label>Fuseau horaire</label>
                <span>{{ authStore.user?.timezone || 'UTC' }}</span>
              </div>
            </div>
          </div>

          <div class="info-section">
            <h3>Préférences</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>Notifications email</label>
                <span>{{ authStore.user?.email_notifications ? 'Activées' : 'Désactivées' }}</span>
              </div>
              <div class="info-item">
                <label>Notifications</label>
                <span>{{ authStore.user?.notifications_enabled ? 'Activées' : 'Désactivées' }}</span>
              </div>
            </div>
          </div>

          <div class="profile-actions">
            <button @click="startEditing" class="btn btn-primary">
              Modifier le profil
            </button>
          </div>
        </div>

        <div class="profile-form" v-else>
          <BaseForm
            title="Modifier le profil"
            description="Mettez à jour vos informations personnelles"
            :fields="profileFields"
            :initial-values="form"
            :on-submit="handleUpdateProfile"
            :loading="authStore.isLoading"
            loading-text="Mise à jour..."
            :general-error="authStore.error || undefined"
          >
            <template #submit-label>Sauvegarder</template>
            <template #footer>
              <div class="form-actions">
                <button type="button" @click="cancelEditing" class="btn btn-secondary">
                  Annuler
                </button>
              </div>
            </template>
          </BaseForm>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseForm from '@/components/BaseForm.vue'

const router = useRouter()
const authStore = useAuthStore()

const isEditing = ref(false)
const form = ref({
  username: '',
  bio: '',
  location: '',
  language: 'fr',
  timezone: 'UTC',
  notifications_enabled: true,
  email_notifications: true
})

const profileFields = [
  {
    name: 'username',
    label: 'Nom d\'utilisateur',
    type: 'text',
    required: true,
    autocomplete: 'username'
  },
  {
    name: 'bio',
    label: 'Biographie',
    type: 'textarea',
    placeholder: 'Parlez-nous de vous...',
    rows: 3
  },
  {
    name: 'location',
    label: 'Localisation',
    type: 'text',
    placeholder: 'Votre ville, pays'
  },
  {
    name: 'language',
    label: 'Langue',
    type: 'select',
    options: [
      { value: 'fr', label: 'Français' },
      { value: 'en', label: 'English' },
      { value: 'es', label: 'Español' },
      { value: 'de', label: 'Deutsch' }
    ]
  },
  {
    name: 'timezone',
    label: 'Fuseau horaire',
    type: 'text',
    placeholder: 'UTC'
  },
  {
    name: 'email_notifications',
    label: 'Notifications par email',
    type: 'checkbox'
  },
  {
    name: 'notifications_enabled',
    label: 'Recevoir des notifications',
    type: 'checkbox'
  }
]


const startEditing = () => {
  if (authStore.user) {
    form.value = {
      username: authStore.user.username || '',
      bio: authStore.user.bio || '',
      location: authStore.user.location || '',
      language: authStore.user.language || 'fr',
      timezone: authStore.user.timezone || 'UTC',
      notifications_enabled: authStore.user.notifications_enabled ?? true,
      email_notifications: authStore.user.email_notifications ?? true
    }
  }
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
  authStore.error = null
}

const handleUpdateProfile = async (formData: Record<string, any>) => {
  const success = await authStore.updateProfile(formData)
  if (success) {
    isEditing.value = false
  }
}

onMounted(async () => {
  if (!authStore.isAuthenticated) {
    router.push('/login')
    return
  }
  
  if (!authStore.user) {
    await authStore.fetchProfile()
  }
})
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f8fafc;
  padding: 2rem;
}

.profile-container {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
}

.profile-header h1 {
  font-size: 2.5rem;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.profile-header p {
  color: #6b7280;
  font-size: 1.1rem;
}

.profile-content {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.info-section {
  margin-bottom: 2rem;
}

.info-section h3 {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
}

.info-item span {
  color: #6b7280;
  padding: 0.5rem 0;
  min-height: 1.5rem;
}

.profile-actions {
  text-align: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e5e7eb;
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

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 1rem;
  }
  
  .info-grid,
  .form-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>