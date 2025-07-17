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
                <label>Niveau d'expertise</label>
                <span>{{ getExpertiseLabel(authStore.user?.expertise_level) }}</span>
              </div>
              <div class="info-item">
                <label>Téléphone</label>
                <span>{{ authStore.user?.phone || 'Non renseigné' }}</span>
              </div>
            </div>
          </div>

          <div class="info-section">
            <h3>Préférences</h3>
            <div class="info-grid">
              <div class="info-item">
                <label>Unités préférées</label>
                <span>{{ getUnitsLabel(authStore.user?.preferred_units) }}</span>
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
          <form @submit.prevent="handleUpdateProfile">
            <div class="form-section">
              <h3>Informations générales</h3>
              <div class="form-grid">
                <div class="form-group">
                  <label for="username">Nom d'utilisateur</label>
                  <input
                    id="username"
                    v-model="form.username"
                    type="text"
                    required
                    :disabled="authStore.isLoading"
                  />
                </div>

                <div class="form-group">
                  <label for="bio">Biographie</label>
                  <textarea
                    id="bio"
                    v-model="form.bio"
                    rows="3"
                    placeholder="Parlez-nous de vous..."
                    :disabled="authStore.isLoading"
                  ></textarea>
                </div>

                <div class="form-group">
                  <label for="location">Localisation</label>
                  <input
                    id="location"
                    v-model="form.location"
                    type="text"
                    placeholder="Votre ville, pays"
                    :disabled="authStore.isLoading"
                  />
                </div>

                <div class="form-group">
                  <label for="expertise_level">Niveau d'expertise</label>
                  <select
                    id="expertise_level"
                    v-model="form.expertise_level"
                    :disabled="authStore.isLoading"
                  >
                    <option value="beginner">Débutant</option>
                    <option value="intermediate">Intermédiaire</option>
                    <option value="advanced">Avancé</option>
                    <option value="expert">Expert</option>
                  </select>
                </div>

                <div class="form-group">
                  <label for="phone">Téléphone</label>
                  <input
                    id="phone"
                    v-model="form.phone"
                    type="tel"
                    placeholder="+33 1 23 45 67 89"
                    :disabled="authStore.isLoading"
                  />
                </div>
              </div>
            </div>

            <div class="form-section">
              <h3>Préférences</h3>
              <div class="form-grid">
                <div class="form-group">
                  <label for="preferred_units">Unités préférées</label>
                  <select
                    id="preferred_units"
                    v-model="form.preferred_units"
                    :disabled="authStore.isLoading"
                  >
                    <option value="metric">Métrique (cm, ml, °C)</option>
                    <option value="imperial">Impérial (in, fl oz, °F)</option>
                  </select>
                </div>

                <div class="form-group">
                  <label class="checkbox-label">
                    <input
                      type="checkbox"
                      v-model="form.notifications_enabled"
                      :disabled="authStore.isLoading"
                    />
                    Recevoir des notifications
                  </label>
                </div>
              </div>
            </div>

            <div class="error-message" v-if="authStore.error">
              {{ authStore.error }}
            </div>

            <div class="form-actions">
              <button type="button" @click="cancelEditing" class="btn btn-secondary">
                Annuler
              </button>
              <button type="submit" class="btn btn-primary" :disabled="authStore.isLoading">
                <span v-if="authStore.isLoading">Mise à jour...</span>
                <span v-else>Sauvegarder</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isEditing = ref(false)
const form = ref({
  username: '',
  bio: '',
  location: '',
  expertise_level: 'beginner',
  phone: '',
  preferred_units: 'metric',
  notifications_enabled: true
})

const getExpertiseLabel = (level: string | undefined) => {
  const labels = {
    beginner: 'Débutant',
    intermediate: 'Intermédiaire',
    advanced: 'Avancé',
    expert: 'Expert'
  }
  return labels[level as keyof typeof labels] || 'Non renseigné'
}

const getUnitsLabel = (units: string | undefined) => {
  const labels = {
    metric: 'Métrique',
    imperial: 'Impérial'
  }
  return labels[units as keyof typeof labels] || 'Métrique'
}

const startEditing = () => {
  if (authStore.user) {
    form.value = {
      username: authStore.user.username,
      bio: authStore.user.bio || '',
      location: authStore.user.location || '',
      expertise_level: authStore.user.expertise_level || 'beginner',
      phone: authStore.user.phone || '',
      preferred_units: authStore.user.preferred_units || 'metric',
      notifications_enabled: authStore.user.notifications_enabled ?? true
    }
  }
  isEditing.value = true
}

const cancelEditing = () => {
  isEditing.value = false
  authStore.error = null
}

const handleUpdateProfile = async () => {
  const success = await authStore.updateProfile(form.value)
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

.form-section {
  margin-bottom: 2rem;
}

.form-section h3 {
  font-size: 1.25rem;
  color: #374151;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e5e7eb;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.1);
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  margin: 0;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 6px;
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 1rem;
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