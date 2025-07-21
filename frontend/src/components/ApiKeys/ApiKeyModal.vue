<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="modal" @click.stop>
      <div class="modal-header">
        <h3>{{ isEditing ? 'Modifier la clé API' : 'Ajouter une clé API' }}</h3>
        <button @click="$emit('close')" class="close-btn">&times;</button>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-body">
        <div class="form-group">
          <label for="service_name">Service</label>
          <select
            id="service_name"
            v-model="form.service_name"
            :disabled="isEditing"
            required
          >
            <option value="">Sélectionnez un service</option>
            <option
              v-for="service in supportedServices"
              :key="service"
              :value="service"
            >
              {{ getServiceDisplayName(service) }}
            </option>
          </select>
          <small class="help-text" v-if="form.service_name">
            {{ getServiceDescription(form.service_name) }}
          </small>
        </div>

        <div class="form-group">
          <label for="key_name">Nom de la clé</label>
          <input
            id="key_name"
            type="text"
            v-model="form.key_name"
            placeholder="Ex: Mon API OpenAI"
            required
            maxlength="100"
          />
          <small class="help-text">Nom descriptif pour identifier cette clé</small>
        </div>

        <div class="form-group" v-if="!isEditing || showApiKeyField">
          <label for="api_key">Clé API</label>
          <div class="api-key-input">
            <input
              id="api_key"
              :type="showApiKey ? 'text' : 'password'"
              v-model="form.api_key"
              :placeholder="getApiKeyPlaceholder(form.service_name)"
              :required="!isEditing"
            />
            <button
              type="button"
              @click="showApiKey = !showApiKey"
              class="toggle-visibility"
              :title="showApiKey ? 'Masquer' : 'Afficher'"
            >
              {{ showApiKey ? '👁️' : '🙈' }}
            </button>
          </div>
          <small class="help-text">
            {{ isEditing ? 'Laissez vide pour conserver la clé actuelle' : 'Votre clé API sera chiffrée et stockée de manière sécurisée' }}
          </small>
        </div>

        <div class="form-group" v-if="isEditing && !showApiKeyField">
          <button
            type="button"
            @click="showApiKeyField = true"
            class="btn-secondary"
          >
            Modifier la clé API
          </button>
        </div>

        <div class="form-group" v-if="isEditing">
          <label class="checkbox-label">
            <input
              type="checkbox"
              v-model="form.is_active"
            />
            Clé active
          </label>
          <small class="help-text">Désactivez temporairement cette clé sans la supprimer</small>
        </div>

        <div class="modal-footer">
          <button type="button" @click="$emit('close')" class="btn-secondary">
            Annuler
          </button>
          <button type="submit" class="btn-primary" :disabled="isLoading">
            {{ isLoading ? 'En cours...' : (isEditing ? 'Modifier' : 'Ajouter') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { ApiKey, CreateApiKeyData, UpdateApiKeyData } from '@/types'
import { useApiKeysStore } from '@/stores/apiKeys'

// Props
interface Props {
  apiKey?: ApiKey | null
  supportedServices: string[]
}

const props = withDefaults(defineProps<Props>(), {
  apiKey: null
})

// Emits
const emit = defineEmits<{
  save: []
  close: []
}>()

// Store
const store = useApiKeysStore()

// State
const isLoading = ref(false)
const showApiKey = ref(false)
const showApiKeyField = ref(false)

const form = ref<CreateApiKeyData & { is_active?: boolean }>({
  service_name: 'openai',
  key_name: '',
  api_key: '',
  is_active: true
})

// Computed
const isEditing = computed(() => !!props.apiKey)

// Methods
const getServiceDisplayName = (service: string): string => {
  const names = {
    openai: 'OpenAI',
    claude: 'Claude (Anthropic)',
    gemini: 'Gemini (Google)',
    huggingface: 'Hugging Face'
  }
  return names[service as keyof typeof names] || service
}

const getServiceDescription = (service: string): string => {
  const descriptions = {
    openai: 'GPT-4, GPT-3.5, DALL-E, Whisper',
    claude: 'Claude 3, Claude 2',
    gemini: 'Gemini Pro, Gemini Ultra',
    huggingface: 'Modèles open-source variés'
  }
  return descriptions[service as keyof typeof descriptions] || ''
}

const getApiKeyPlaceholder = (service: string): string => {
  const placeholders = {
    openai: 'sk-...',
    claude: 'sk-ant-...',
    gemini: 'Votre clé Gemini',
    huggingface: 'hf_...'
  }
  return placeholders[service as keyof typeof placeholders] || 'Votre clé API'
}

const handleSubmit = async (): Promise<void> => {
  isLoading.value = true
  
  try {
    if (isEditing.value && props.apiKey) {
      // Mode édition
      const updateData: UpdateApiKeyData = {
        key_name: form.value.key_name,
        is_active: form.value.is_active
      }
      
      // Ajouter la clé API seulement si elle a été modifiée
      if (showApiKeyField.value && form.value.api_key.trim()) {
        updateData.api_key = form.value.api_key
      }
      
      const success = await store.updateApiKey(props.apiKey.id, updateData)
      if (success) {
        emit('save')
      }
    } else {
      // Mode création
      if (!form.value.api_key.trim()) {
        return
      }
      
      const success = await store.createApiKey({
        service_name: form.value.service_name,
        key_name: form.value.key_name,
        api_key: form.value.api_key
      })
      
      if (success) {
        emit('save')
      }
    }
  } finally {
    isLoading.value = false
  }
}

const handleOverlayClick = (): void => {
  emit('close')
}

// Lifecycle
onMounted(() => {
  if (props.apiKey) {
    // Mode édition : pré-remplir le formulaire
    form.value = {
      service_name: props.apiKey.service_name,
      key_name: props.apiKey.key_name,
      api_key: '',
      is_active: props.apiKey.is_active
    }
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  color: #2d3748;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #718096;
  width: 2rem;
  height: 2rem;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background-color: #f7fafc;
  color: #2d3748;
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2d3748;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1);
}

.api-key-input {
  position: relative;
}

.toggle-visibility {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  font-size: 1rem;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.toggle-visibility:hover {
  background-color: #f7fafc;
}

.help-text {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #718096;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-weight: 400 !important;
}

.checkbox-label input[type="checkbox"] {
  width: auto !important;
  margin: 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}

.btn-primary,
.btn-secondary {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.btn-primary {
  background-color: #4299e1;
  color: white;
  border-color: #4299e1;
}

.btn-primary:hover:not(:disabled) {
  background-color: #3182ce;
  border-color: #3182ce;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background-color: transparent;
  color: #4a5568;
  border-color: #d1d5db;
}

.btn-secondary:hover {
  background-color: #f7fafc;
  border-color: #a0aec0;
}

@media (max-width: 640px) {
  .modal {
    margin: 0.5rem;
  }
  
  .modal-header,
  .modal-body {
    padding: 1rem;
  }
  
  .modal-footer {
    flex-direction: column;
  }
  
  .btn-primary,
  .btn-secondary {
    width: 100%;
  }
}
</style>