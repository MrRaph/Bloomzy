<template>
  <div class="my-plants-page">
    <div class="page-header">
      <h1>Mes Plantes</h1>
      <p>Gérez votre collection personnelle de plantes d'intérieur</p>
      <button @click="showAddForm = true" class="btn btn-primary">
        + Ajouter une plante
      </button>
    </div>

    <!-- Statistiques rapides -->
    <div class="stats-grid" v-if="!store.isLoading && plants.length > 0">
      <div class="stat-card">
        <div class="stat-icon">🌱</div>
        <div class="stat-content">
          <h3>{{ plants.length }}</h3>
          <p>Plante{{ plants.length > 1 ? 's' : '' }} au total</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">💚</div>
        <div class="stat-content">
          <h3>{{ store.healthyPlants.length }}</h3>
          <p>En bonne santé</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⚠️</div>
        <div class="stat-content">
          <h3>{{ store.plantsNeedingAttention.length }}</h3>
          <p>Nécessitent attention</p>
        </div>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="store.error" class="error-message">
      {{ store.error }}
    </div>

    <!-- Indicateur de chargement -->
    <div v-if="store.isLoading" class="loading">
      <p>Chargement de vos plantes...</p>
    </div>

    <!-- Liste des plantes -->
    <div v-else-if="plants.length > 0" class="plants-grid">
                <PlantCard
            v-for="plant in store.plants"
            :key="plant.id"
            :plant="plant"
            @edit="(plant) => editPlant(plant)"
            @delete="(plant) => handleDeletePlant(plant)"
            @water="(plant) => openWateringModal(plant)"
          />
    </div>

    <!-- Message si aucune plante -->
    <div v-else-if="!store.isLoading" class="empty-state">
      <div class="empty-icon">🪴</div>
      <h3>Aucune plante enregistrée</h3>
      <p>Commencez par ajouter votre première plante à votre collection !</p>
      <button @click="showAddForm = true" class="btn btn-primary">
        Ajouter ma première plante
      </button>
    </div>

    <!-- Formulaire d'ajout/modification -->
    <div v-if="showAddForm || editingPlant" class="modal-overlay" @click="closeForm">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ editingPlant ? 'Modifier' : 'Ajouter' }} une plante</h2>
          <button @click="closeForm" class="close-btn">&times;</button>
        </div>
        
        <BaseForm
          :title="editingPlant ? 'Modifier une plante' : 'Ajouter une plante'"
          :description="editingPlant ? 'Modifiez les informations de votre plante' : 'Ajoutez une nouvelle plante à votre collection'"
          :fields="plantFields"
          :initial-values="form"
          :on-submit="submitForm"
        >
          <template #submit-label>{{ editingPlant ? 'Enregistrer' : 'Ajouter' }}</template>
          <template #footer>
            <div class="form-actions">
              <button type="button" @click="closeForm" class="btn btn-secondary">
                Annuler
              </button>
            </div>
          </template>
        </BaseForm>
      </div>
    </div>

    <!-- Modal d'arrosage -->
    <div v-if="wateringPlant" class="modal-overlay" @click="closeWateringModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>Arroser {{ wateringPlant.custom_name }}</h2>
          <button @click="closeWateringModal" class="close-btn">&times;</button>
        </div>
        
        <BaseForm
          title="Enregistrer un arrosage"
          description="Notez les détails de l'arrosage pour un meilleur suivi"
          :fields="wateringFields"
          :initial-values="wateringForm"
          :on-submit="submitWatering"
        >
          <template #submit-label>Enregistrer l'arrosage</template>
          <template #footer>
            <div class="form-actions">
              <button type="button" @click="closeWateringModal" class="btn btn-secondary">
                Annuler
              </button>
            </div>
          </template>
        </BaseForm>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useMyPlantsStore } from '@/stores/myPlants'
import { useNotifications } from '@/composables/useNotifications'
import { fetchIndoorPlants } from '@/services/api'
import BaseForm from '@/components/BaseForm.vue'
import PlantCard from '@/components/PlantCard.vue'
import type { UserPlant } from '@/types'

const store = useMyPlantsStore()
const { plantActions, error: notifyError } = useNotifications()
const plants = computed(() => store.plants)

const showAddForm = ref(false)
const editingPlant = ref<UserPlant | null>(null)
const wateringPlant = ref<UserPlant | null>(null)

const form = ref({
  species_id: '',
  custom_name: '',
  location: '',
  pot_size: '',
  health_status: 'healthy',
  notes: ''
})

const wateringForm = ref({
  amount_ml: '',
  water_type: 'tap',
  notes: ''
})

const speciesOptions = ref<Array<{ value: string; label: string }>>([])

// Champs du formulaire de plante
const plantFields = [
  {
    name: 'species_id',
    label: 'Espèce de plante',
    type: 'select',
    required: true,
    options: speciesOptions.value,
    placeholder: 'Sélectionnez une espèce'
  },
  {
    name: 'custom_name',
    label: 'Nom personnalisé',
    type: 'text',
    required: true,
    placeholder: 'Ex: Mon Ficus du salon'
  },
  {
    name: 'location',
    label: 'Emplacement',
    type: 'text',
    placeholder: 'Ex: Salon, Bureau, Chambre'
  },
  {
    name: 'pot_size',
    label: 'Taille du pot',
    type: 'select',
    options: [
      { value: 'Petit', label: 'Petit (≤ 15cm)' },
      { value: 'Moyen', label: 'Moyen (15-25cm)' },
      { value: 'Grand', label: 'Grand (25-35cm)' },
      { value: 'Très grand', label: 'Très grand (> 35cm)' }
    ]
  },
  {
    name: 'health_status',
    label: 'État de santé',
    type: 'select',
    required: true,
    options: [
      { value: 'healthy', label: '💚 Bonne santé' },
      { value: 'sick', label: '😷 Malade' },
      { value: 'dying', label: '💔 Dépérit' },
      { value: 'dead', label: '💀 Morte' }
    ]
  },
  {
    name: 'notes',
    label: 'Notes',
    type: 'textarea',
    placeholder: 'Observations particulières...'
  }
]

// Champs du formulaire d'arrosage
const wateringFields = [
  {
    name: 'amount_ml',
    label: 'Quantité d\'eau (ml)',
    type: 'number',
    placeholder: 'Ex: 250'
  },
  {
    name: 'water_type',
    label: 'Type d\'eau',
    type: 'select',
    options: [
      { value: 'tap', label: 'Eau du robinet' },
      { value: 'filtered', label: 'Eau filtrée' },
      { value: 'rainwater', label: 'Eau de pluie' },
      { value: 'distilled', label: 'Eau distillée' },
      { value: 'other', label: 'Autre' }
    ]
  },
  {
    name: 'notes',
    label: 'Notes',
    type: 'textarea',
    placeholder: 'Observations sur l\'arrosage...'
  }
]

onMounted(async () => {
  await store.fetchPlants()
  await loadSpeciesOptions()
})

const loadSpeciesOptions = async () => {
  try {
    const species = await fetchIndoorPlants()
    speciesOptions.value = species.map(s => ({
      value: s.id.toString(),
      label: `${s.scientific_name} (${s.common_names})`
    }))
    
    // Met à jour les options dans le champ
    const speciesField = plantFields.find(f => f.name === 'species_id')
    if (speciesField) {
      speciesField.options = speciesOptions.value
    }
  } catch (error) {
    console.error('Erreur lors du chargement des espèces:', error)
  }
}

const editPlant = (plant: UserPlant) => {
  editingPlant.value = plant
  form.value = {
    species_id: plant.species_id.toString(),
    custom_name: plant.custom_name,
    location: plant.location || '',
    pot_size: plant.pot_size || '',
    health_status: plant.health_status,
    notes: plant.notes || ''
  }
  showAddForm.value = false
}

const handleDeletePlant = async (plant: UserPlant) => {
  if (confirm(`Êtes-vous sûr de vouloir supprimer ${plant.custom_name} ?`)) {
    const success = await store.deletePlant(plant.id)
    if (success) {
      plantActions.deleted(plant.custom_name)
    } else {
      notifyError('Impossible de supprimer la plante. Réessayez plus tard.')
    }
  }
}

const openWateringModal = (plant: UserPlant) => {
  wateringPlant.value = plant
  wateringForm.value = {
    amount_ml: '',
    water_type: 'tap',
    notes: ''
  }
}

const closeWateringModal = () => {
  wateringPlant.value = null
}

const submitForm = async (formData: Record<string, any>) => {
  const plantData = {
    species_id: parseInt(formData.species_id),
    custom_name: formData.custom_name,
    location: formData.location || undefined,
    pot_size: formData.pot_size || undefined,
    health_status: formData.health_status,
    notes: formData.notes || undefined
  }

  let success = false
  if (editingPlant.value) {
    success = await store.updatePlant(editingPlant.value.id, plantData)
  } else {
    success = await store.addPlant(plantData)
  }

  if (success) {
    closeForm()
  }
}

const submitWatering = async (formData: Record<string, any>) => {
  if (!wateringPlant.value) return

  const wateringData = {
    plant_id: wateringPlant.value.id,
    watered_at: new Date().toISOString(),
    amount_ml: formData.amount_ml ? parseInt(formData.amount_ml) : undefined,
    water_type: formData.water_type,
    notes: formData.notes || undefined
  }

  try {
    await store.addWatering(wateringData)
    closeWateringModal()
  } catch (error) {
    console.error('Erreur lors de l\'enregistrement de l\'arrosage:', error)
  }
}

const closeForm = () => {
  showAddForm.value = false
  editingPlant.value = null
  form.value = {
    species_id: '',
    custom_name: '',
    location: '',
    pot_size: '',
    health_status: 'healthy',
    notes: ''
  }
}
</script>

<style scoped>
.my-plants-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #4a5568;
  margin-bottom: 1.5rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #2d3748;
}

.stat-content p {
  margin: 0;
  color: #4a5568;
}

.plants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.plant-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.plant-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.plant-photo {
  height: 200px;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.plant-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.plant-placeholder {
  font-size: 3rem;
  color: #a0aec0;
}

.plant-info {
  padding: 1.5rem;
}

.plant-info h3 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
}

.plant-species {
  color: #4a5568;
  font-style: italic;
  margin: 0 0 0.5rem 0;
}

.plant-location {
  color: #718096;
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
}

.plant-status {
  margin-bottom: 1rem;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status-healthy {
  background: #c6f6d5;
  color: #22543d;
}

.status-sick {
  background: #fed7d7;
  color: #742a2a;
}

.status-dying {
  background: #feebc8;
  color: #744210;
}

.status-dead {
  background: #e2e8f0;
  color: #2d3748;
}

.plant-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #4a5568;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h2 {
  margin: 0;
  color: #2d3748;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #a0aec0;
  transition: color 0.2s;
}

.close-btn:hover {
  color: #4a5568;
}

.error-message {
  background: #fed7d7;
  color: #742a2a;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #4a5568;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: #4299e1;
  color: white;
}

.btn-primary:hover {
  background: #3182ce;
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
}

.btn-danger {
  background: #e53e3e;
  color: white;
}

.btn-danger:hover {
  background: #c53030;
}

.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
