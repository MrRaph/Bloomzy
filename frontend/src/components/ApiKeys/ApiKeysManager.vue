<template>
  <div class="api-keys-manager">
    <div class="header">
      <h2>Gestion des Clés API</h2>
      <button @click="showCreateModal = true" class="btn-primary">
        <span class="icon">+</span>
        Ajouter une clé
      </button>
    </div>

    <div class="description">
      <p>Gérez vos clés API pour les services d'intelligence artificielle. Ces clés sont chiffrées et stockées de manière sécurisée.</p>
    </div>

    <div v-if="store.isLoading" class="loading">
      Chargement des clés API...
    </div>

    <div v-else-if="store.apiKeys.length === 0" class="empty-state">
      <div class="empty-icon">🔑</div>
      <h3>Aucune clé API configurée</h3>
      <p>Ajoutez votre première clé API pour commencer à utiliser les fonctionnalités d'intelligence artificielle.</p>
      <button @click="showCreateModal = true" class="btn-primary">
        Ajouter ma première clé
      </button>
    </div>

    <div v-else class="api-keys-list">
      <div
        v-for="apiKey in store.apiKeys"
        :key="apiKey.id"
        class="api-key-card"
        :class="{ inactive: !apiKey.is_active }"
      >
        <div class="card-header">
          <div class="service-info">
            <div class="service-icon">
              {{ getServiceIcon(apiKey.service_name) }}
            </div>
            <div class="service-details">
              <h4>{{ apiKey.key_name }}</h4>
              <span class="service-name">{{ getServiceDisplayName(apiKey.service_name) }}</span>
            </div>
          </div>
          <div class="card-actions">
            <button
              @click="toggleStatus(apiKey.id)"
              :class="apiKey.is_active ? 'btn-status-active' : 'btn-status-inactive'"
              :title="apiKey.is_active ? 'Désactiver' : 'Activer'"
            >
              {{ apiKey.is_active ? '✓' : '⏸' }}
            </button>
            <button @click="testKey(apiKey.id)" class="btn-test" title="Tester la clé">
              🧪
            </button>
            <button @click="editKey(apiKey)" class="btn-edit" title="Modifier">
              ✏️
            </button>
            <button @click="deleteKey(apiKey.id)" class="btn-delete" title="Supprimer">
              🗑️
            </button>
          </div>
        </div>
        
        <div class="card-details">
          <div class="detail-item">
            <span class="label">Créée le:</span>
            <span class="value">{{ formatDate(apiKey.created_at) }}</span>
          </div>
          <div class="detail-item" v-if="apiKey.last_used_at">
            <span class="label">Dernière utilisation:</span>
            <span class="value">{{ formatDate(apiKey.last_used_at) }}</span>
          </div>
          <div class="detail-item">
            <span class="label">Statut:</span>
            <span class="status" :class="apiKey.is_active ? 'active' : 'inactive'">
              {{ apiKey.is_active ? 'Active' : 'Inactive' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de création/édition -->
    <ApiKeyModal
      v-if="showCreateModal || editingKey"
      :api-key="editingKey"
      :supported-services="store.supportedServices"
      @save="handleSave"
      @close="closeModal"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { ApiKey } from '@/types'
import { useApiKeysStore } from '@/stores/apiKeys'
import ApiKeyModal from './ApiKeyModal.vue'

const store = useApiKeysStore()

// State
const showCreateModal = ref(false)
const editingKey = ref<ApiKey | null>(null)

// Methods
const getServiceIcon = (service: string): string => {
  const icons = {
    openai: '🤖',
    claude: '🧠',
    gemini: '💎',
    huggingface: '🤗'
  }
  return icons[service as keyof typeof icons] || '🔑'
}

const getServiceDisplayName = (service: string): string => {
  const names = {
    openai: 'OpenAI',
    claude: 'Claude',
    gemini: 'Gemini',
    huggingface: 'Hugging Face'
  }
  return names[service as keyof typeof names] || service
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const toggleStatus = async (id: number): Promise<void> => {
  await store.toggleApiKeyStatus(id)
}

const testKey = async (id: number): Promise<void> => {
  await store.testApiKey(id)
}

const editKey = (apiKey: ApiKey): void => {
  editingKey.value = apiKey
}

const deleteKey = async (id: number): Promise<void> => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette clé API ?')) {
    await store.deleteApiKey(id)
  }
}

const handleSave = async (): Promise<void> => {
  await store.fetchApiKeys() // Recharger la liste après sauvegarde
  closeModal()
}

const closeModal = (): void => {
  showCreateModal.value = false
  editingKey.value = null
}

// Lifecycle
onMounted(() => {
  store.init()
})
</script>

<style scoped>
.api-keys-manager {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.header h2 {
  margin: 0;
  color: #2d3748;
}

.description {
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #4299e1;
}

.description p {
  margin: 0;
  color: #4a5568;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: #718096;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #718096;
  margin-bottom: 2rem;
}

.api-keys-list {
  display: grid;
  gap: 1rem;
}

.api-key-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.api-key-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.api-key-card.inactive {
  opacity: 0.6;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.service-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.service-icon {
  font-size: 2rem;
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f7fafc;
  border-radius: 8px;
}

.service-details h4 {
  margin: 0 0 0.25rem 0;
  color: #2d3748;
  font-weight: 600;
}

.service-name {
  color: #718096;
  font-size: 0.875rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.card-actions button {
  width: 2rem;
  height: 2rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.btn-status-active {
  background-color: #48bb78;
  color: white;
}

.btn-status-inactive {
  background-color: #a0aec0;
  color: white;
}

.btn-test {
  background-color: #4299e1;
  color: white;
}

.btn-edit {
  background-color: #ed8936;
  color: white;
}

.btn-delete {
  background-color: #f56565;
  color: white;
}

.card-actions button:hover {
  transform: scale(1.05);
}

.card-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.label {
  font-size: 0.75rem;
  color: #718096;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.value {
  color: #2d3748;
  font-weight: 500;
}

.status.active {
  color: #38a169;
  font-weight: 600;
}

.status.inactive {
  color: #a0aec0;
  font-weight: 600;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: #3182ce;
  transform: translateY(-1px);
}

.icon {
  font-size: 1.25rem;
}

@media (max-width: 768px) {
  .api-keys-manager {
    padding: 1rem;
  }
  
  .header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .card-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .card-actions {
    justify-content: center;
  }
}
</style>