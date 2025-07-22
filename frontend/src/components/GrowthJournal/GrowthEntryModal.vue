<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h3>{{ isEditing ? 'Modifier l\'entrée' : 'Nouvelle entrée de croissance' }}</h3>
        <button @click="$emit('close')" class="btn-close">&times;</button>
      </div>

      <form @submit.prevent="submitForm" class="modal-body">
        <div class="form-section">
          <div class="form-group">
            <label>Type d'entrée *</label>
            <select v-model="form.entry_type" required :disabled="isEditing">
              <option value="">Sélectionner un type</option>
              <option value="photo">Photo</option>
              <option value="measurement">Mesures</option>
              <option value="observation">Observation</option>
            </select>
          </div>

          <div class="form-group">
            <label>Date</label>
            <input 
              type="date" 
              v-model="form.entry_date"
              :max="today"
            />
          </div>
        </div>

        <!-- Photo Section -->
        <div v-if="form.entry_type === 'photo'" class="form-section">
          <h4>📸 Photo</h4>
          <div class="form-group">
            <label>Photo *</label>
            <input 
              type="file" 
              accept="image/*" 
              @change="handleFileChange"
              :required="!isEditing"
            />
            <div v-if="selectedFile" class="file-preview">
              Fichier sélectionné : {{ selectedFile.name }}
            </div>
          </div>
          
          <div class="form-group">
            <label>Description de la photo</label>
            <textarea 
              v-model="form.photo_description" 
              rows="2"
              placeholder="Décrivez cette photo..."
            ></textarea>
          </div>
        </div>

        <!-- Measurements Section -->
        <div v-if="form.entry_type === 'measurement' || form.entry_type === 'observation'" class="form-section">
          <h4>📏 Mesures</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Hauteur (cm)</label>
              <input 
                type="number" 
                v-model="form.height_cm" 
                min="0" 
                max="1000"
                step="0.1"
              />
            </div>
            <div class="form-group">
              <label>Largeur (cm)</label>
              <input 
                type="number" 
                v-model="form.width_cm" 
                min="0" 
                max="1000"
                step="0.1"
              />
            </div>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>Nombre de feuilles</label>
              <input 
                type="number" 
                v-model="form.leaf_count" 
                min="0" 
                max="10000"
              />
            </div>
            <div class="form-group">
              <label>Nombre de tiges</label>
              <input 
                type="number" 
                v-model="form.stem_count" 
                min="0" 
                max="1000"
              />
            </div>
          </div>
        </div>

        <!-- Health Section -->
        <div v-if="form.entry_type === 'measurement' || form.entry_type === 'observation'" class="form-section">
          <h4>🌿 État de santé</h4>
          <div class="form-row">
            <div class="form-group">
              <label>Couleur des feuilles</label>
              <select v-model="form.leaf_color">
                <option value="">Non spécifié</option>
                <option value="green">Vert</option>
                <option value="yellow">Jaune</option>
                <option value="brown">Marron</option>
                <option value="red">Rouge</option>
                <option value="purple">Violet</option>
                <option value="variegated">Panaché</option>
              </select>
            </div>
            <div class="form-group">
              <label>Fermeté des tiges</label>
              <select v-model="form.stem_firmness">
                <option value="">Non spécifié</option>
                <option value="firm">Ferme</option>
                <option value="soft">Souple</option>
                <option value="brittle">Cassant</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="checkbox-group">
              <input type="checkbox" v-model="form.has_flowers" />
              Présence de fleurs
            </label>
          </div>

          <div class="form-group">
            <label class="checkbox-group">
              <input type="checkbox" v-model="form.has_fruits" />
              Présence de fruits
            </label>
          </div>
        </div>

        <!-- Notes Section -->
        <div class="form-section">
          <h4>📝 Notes</h4>
          <div v-if="form.entry_type === 'measurement' || form.entry_type === 'observation'" class="form-group">
            <label>Notes de santé</label>
            <textarea 
              v-model="form.health_notes" 
              rows="2"
              placeholder="Notes sur l'état de santé de la plante..."
            ></textarea>
          </div>

          <div v-if="form.entry_type === 'measurement' || form.entry_type === 'observation'" class="form-group">
            <label>Notes de croissance</label>
            <textarea 
              v-model="form.growth_notes" 
              rows="2"
              placeholder="Notes sur la croissance et le développement..."
            ></textarea>
          </div>

          <div class="form-group">
            <label>Observations personnelles</label>
            <textarea 
              v-model="form.user_observations" 
              rows="3"
              placeholder="Vos observations générales..."
            ></textarea>
          </div>
        </div>
      </form>

      <div class="modal-footer">
        <button type="button" @click="$emit('close')" class="btn-secondary">
          Annuler
        </button>
        <button 
          type="button" 
          @click="submitForm" 
          :disabled="!isFormValid || submitting"
          class="btn-primary"
        >
          {{ submitting ? 'En cours...' : (isEditing ? 'Modifier' : 'Créer') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import type { GrowthEntry, CreateGrowthEntryData, UpdateGrowthEntryData } from '@/types'
import { growthJournalApi } from '@/services/api'
import { useNotifications } from '@/composables/useNotifications'

const props = defineProps<{
  entry?: GrowthEntry | null
  plantId: number
}>()

const emit = defineEmits<{
  close: []
  success: []
}>()

const { addNotification } = useNotifications()

const isEditing = computed(() => !!props.entry)
const submitting = ref(false)
const selectedFile = ref<File | null>(null)

const today = new Date().toISOString().split('T')[0]

const form = reactive<CreateGrowthEntryData & UpdateGrowthEntryData>({
  entry_type: 'observation',
  entry_date: today,
  photo_description: '',
  height_cm: undefined,
  width_cm: undefined,
  leaf_count: undefined,
  stem_count: undefined,
  leaf_color: undefined,
  stem_firmness: undefined,
  has_flowers: false,
  has_fruits: false,
  health_notes: '',
  growth_notes: '',
  user_observations: ''
})

const isFormValid = computed(() => {
  if (!form.entry_type) return false
  if (form.entry_type === 'photo' && !selectedFile.value && !isEditing.value) return false
  return true
})

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement
  selectedFile.value = target.files?.[0] || null
}

const submitForm = async () => {
  if (!isFormValid.value || submitting.value) return

  submitting.value = true
  try {
    if (isEditing.value && props.entry) {
      // Update existing entry
      const updateData: UpdateGrowthEntryData = { ...form }
      // Clean up empty values
      Object.keys(updateData).forEach(key => {
        const value = (updateData as any)[key]
        if (value === '' || value === undefined || value === null) {
          delete (updateData as any)[key]
        }
      })

      await growthJournalApi.update(props.plantId, props.entry.id, updateData)
      addNotification({
        type: 'success',
        message: 'Entrée modifiée avec succès'
      })
    } else {
      // Create new entry
      if (form.entry_type === 'photo' && selectedFile.value) {
        // Upload photo with entry
        const photoData = { ...form }
        delete (photoData as any).entry_type // Remove entry_type as it's set automatically
        await growthJournalApi.uploadPhoto(props.plantId, selectedFile.value, photoData)
      } else {
        // Create regular entry
        const createData: CreateGrowthEntryData = { ...form }
        // Clean up empty values
        Object.keys(createData).forEach(key => {
          const value = (createData as any)[key]
          if (value === '' || value === undefined || value === null) {
            delete (createData as any)[key]
          }
        })
        await growthJournalApi.create(props.plantId, createData)
      }
      
      addNotification({
        type: 'success',
        message: 'Entrée créée avec succès'
      })
    }

    emit('success')
  } catch (error) {
    addNotification({
      type: 'error',
      message: isEditing.value ? 'Erreur lors de la modification' : 'Erreur lors de la création'
    })
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  if (props.entry) {
    // Populate form with existing entry data
    Object.assign(form, {
      entry_type: props.entry.entry_type,
      entry_date: props.entry.entry_date,
      photo_description: props.entry.photo_description || '',
      height_cm: props.entry.height_cm,
      width_cm: props.entry.width_cm,
      leaf_count: props.entry.leaf_count,
      stem_count: props.entry.stem_count,
      leaf_color: props.entry.leaf_color || undefined,
      stem_firmness: props.entry.stem_firmness || undefined,
      has_flowers: props.entry.has_flowers || false,
      has_fruits: props.entry.has_fruits || false,
      health_notes: props.entry.health_notes || '',
      growth_notes: props.entry.growth_notes || '',
      user_observations: props.entry.user_observations || ''
    })
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
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  max-width: 600px;
  width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  color: #2d5a27;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-body {
  padding: 20px;
}

.form-section {
  margin-bottom: 25px;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.form-section:last-child {
  border-bottom: none;
  margin-bottom: 0;
}

.form-section h4 {
  color: #2d5a27;
  margin: 0 0 15px 0;
  font-size: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group {
  margin-bottom: 15px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  color: #333;
}

.checkbox-group {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  margin: 0;
}

input[type="text"],
input[type="email"],
input[type="number"],
input[type="date"],
input[type="file"],
select,
textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #4CAF50;
}

.file-preview {
  margin-top: 5px;
  padding: 5px;
  background: #f9f9f9;
  border-radius: 4px;
  font-size: 13px;
  color: #666;
}

.modal-footer {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #45a049;
}

.btn-primary:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background: #eeeeee;
}
</style>