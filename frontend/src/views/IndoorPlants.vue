<template>
  <div class="indoor-plants-page">
    <!-- En-tête de page -->
    <div class="page-header">
      <div class="header-content">
        <div class="header-text">
          <h1>📚 Catalogue des Plantes</h1>
          <p>Découvrez notre collection d'espèces de plantes d'intérieur avec leurs caractéristiques détaillées</p>
        </div>
        <button @click="showAddForm = true" class="btn btn-primary">
          <span class="btn-icon">🌱</span>
          Ajouter une espèce
        </button>
      </div>
    </div>

    <!-- Barre de recherche et filtres -->
    <div class="search-section">
      <div class="search-bar">
        <div class="search-input-group">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Rechercher par nom, famille ou difficulté..."
            class="search-input"
            @input="onSearchInput"
          />
          <button 
            v-if="searchQuery" 
            @click="clearSearch" 
            class="clear-search-btn"
            title="Effacer la recherche"
          >
            ✕
          </button>
        </div>
      </div>
      
      <!-- Filtres rapides -->
      <div class="quick-filters">
        <button 
          v-for="filter in quickFilters" 
          :key="filter.key"
          @click="toggleFilter(filter.key)"
          :class="['filter-btn', { active: activeFilters.includes(filter.key) }]"
        >
          <span class="filter-icon">{{ filter.icon }}</span>
          {{ filter.label }}
        </button>
      </div>
    </div>

    <!-- Statistiques du catalogue -->
    <div class="stats-grid" v-if="!store.loading && plants.length > 0">
      <div class="stat-card">
        <div class="stat-icon">🌿</div>
        <div class="stat-content">
          <h3>{{ filteredPlants.length }}</h3>
          <p>{{ searchQuery || activeFilters.length ? 'Résultat(s)' : 'Espèce(s) totale(s)' }}</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🌱</div>
        <div class="stat-content">
          <h3>{{ easyPlants.length }}</h3>
          <p>Faciles</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🏆</div>
        <div class="stat-content">
          <h3>{{ challengingPlants.length }}</h3>
          <p>Défis</p>
        </div>
      </div>
    </div>

    <!-- Message d'erreur -->
    <div v-if="store.error" class="error-message">
      <span class="error-icon">⚠️</span>
      {{ store.error }}
    </div>

    <!-- Indicateur de chargement -->
    <div v-if="store.loading" class="loading">
      <div class="loading-spinner"></div>
      <p>Chargement du catalogue...</p>
    </div>

    <!-- Catalogue des plantes -->
    <div v-else-if="filteredPlants.length > 0" class="plants-catalog">
      <div class="catalog-header">
        <h2>
          {{ searchQuery || activeFilters.length > 0 ? 
              `${filteredPlants.length} résultat(s) trouvé(s)` : 
              `${plants.length} espèce(s) dans le catalogue` 
          }}
        </h2>
        <div class="view-controls">
          <button 
            @click="viewMode = 'grid'" 
            :class="['view-btn', { active: viewMode === 'grid' }]"
            title="Vue grille"
          >
            ⊞
          </button>
          <button 
            @click="viewMode = 'list'" 
            :class="['view-btn', { active: viewMode === 'list' }]"
            title="Vue liste"
          >
            ≡
          </button>
        </div>
      </div>

      <div :class="['plants-grid', viewMode]">
        <div 
          v-for="plant in filteredPlants" 
          :key="plant.id"
          :class="['plant-card', viewMode]"
        >
          <!-- Image de la plante -->
          <div class="plant-image">
            <div class="plant-placeholder">
              <span class="placeholder-icon">🌿</span>
            </div>
            <div class="difficulty-badge" :class="`difficulty-${getDifficultyLevel(plant)}`">
              {{ getDifficultyIcon(plant) }}
            </div>
          </div>

          <!-- Informations de la plante -->
          <div class="plant-info">
            <h3 class="plant-name">{{ plant.name }}</h3>
            <p class="plant-scientific">{{ plant.species }}</p>
            
            <div class="plant-meta">
              <span v-if="plant.family" class="meta-tag">
                <span class="meta-icon">🏛️</span>
                {{ plant.family }}
              </span>
              <span v-if="plant.difficulty" class="meta-tag difficulty">
                <span class="meta-icon">{{ getDifficultyIcon(plant) }}</span>
                {{ plant.difficulty }}
              </span>
            </div>

            <!-- Actions -->
            <div class="plant-actions">
              <button 
                @click="viewPlantDetails(plant)" 
                class="action-btn action-btn--primary"
                title="Voir les détails"
              >
                <span class="btn-icon">👁️</span>
                <span v-if="viewMode === 'list'">Détails</span>
              </button>
              <button 
                @click="editPlant(plant)" 
                class="action-btn action-btn--secondary"
                title="Modifier cette espèce"
              >
                <span class="btn-icon">✏️</span>
                <span v-if="viewMode === 'list'">Modifier</span>
              </button>
              <button 
                @click="deletePlant(plant.id)" 
                class="action-btn action-btn--danger"
                title="Supprimer cette espèce"
              >
                <span class="btn-icon">🗑️</span>
                <span v-if="viewMode === 'list'">Supprimer</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- État vide -->
    <div v-else-if="!store.loading" class="empty-state">
      <div class="empty-content">
        <div class="empty-icon">
          {{ searchQuery || activeFilters.length > 0 ? '🔍' : '📚' }}
        </div>
        <h3>
          {{ searchQuery || activeFilters.length > 0 ? 
              'Aucun résultat trouvé' : 
              'Catalogue vide' 
          }}
        </h3>
        <p>
          {{ searchQuery || activeFilters.length > 0 ? 
              'Essayez avec d\'autres termes de recherche ou filtres' : 
              'Commencez par ajouter votre première espèce de plante au catalogue' 
          }}
        </p>
        <div class="empty-actions">
          <button 
            v-if="searchQuery || activeFilters.length > 0"
            @click="resetFilters" 
            class="btn btn-secondary"
          >
            Réinitialiser les filtres
          </button>
          <button @click="showAddForm = true" class="btn btn-primary">
            <span class="btn-icon">🌱</span>
            Ajouter une espèce
          </button>
        </div>
      </div>
    </div>

    <!-- Modal de formulaire d'ajout/modification -->
    <div v-if="showAddForm || editingPlant" class="modal-overlay" @click="closeForm">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>
            <span class="modal-icon">{{ editingPlant ? '✏️' : '🌱' }}</span>
            {{ editingPlant ? 'Modifier une espèce' : 'Ajouter une espèce' }}
          </h2>
          <button @click="closeForm" class="close-btn" title="Fermer">&times;</button>
        </div>
        
        <BaseForm
          :title="editingPlant ? 'Modifier une espèce' : 'Ajouter une espèce'"
          :description="editingPlant ? 'Modifiez les informations de cette espèce' : 'Ajoutez une nouvelle espèce au catalogue'"
          :fields="plantFields"
          :initial-values="form"
          :on-submit="submitForm"
        >
          <template #submit-label>
            <span class="btn-icon">{{ editingPlant ? '💾' : '➕' }}</span>
            {{ editingPlant ? 'Enregistrer' : 'Ajouter' }}
          </template>
          <template #footer>
            <div class="form-actions">
              <button type="button" @click="closeForm" class="btn btn-secondary">
                <span class="btn-icon">❌</span>
                Annuler
              </button>
            </div>
          </template>
        </BaseForm>
      </div>
    </div>

    <!-- Modal de détails de plante -->
    <div v-if="selectedPlant" class="modal-overlay" @click="closeDetails">
      <div class="modal-content modal-content--large" @click.stop>
        <div class="modal-header">
          <h2>
            <span class="modal-icon">🌿</span>
            {{ selectedPlant.name }}
          </h2>
          <button @click="closeDetails" class="close-btn" title="Fermer">&times;</button>
        </div>
        
        <div class="plant-details">
          <div class="details-image">
            <div class="plant-placeholder large">
              <span class="placeholder-icon">🌿</span>
              <p>Image non disponible</p>
            </div>
          </div>
          
          <div class="details-info">
            <div class="detail-section">
              <h3>🔬 Classification</h3>
              <div class="detail-grid">
                <div class="detail-item">
                  <strong>Nom scientifique :</strong>
                  <span>{{ selectedPlant.species }}</span>
                </div>
                <div class="detail-item" v-if="selectedPlant.family">
                  <strong>Famille :</strong>
                  <span>{{ selectedPlant.family }}</span>
                </div>
              </div>
            </div>
            
            <div class="detail-section" v-if="selectedPlant.difficulty">
              <h3>📊 Niveau de difficulté</h3>
              <div class="difficulty-info">
                <span class="difficulty-badge large" :class="`difficulty-${getDifficultyLevel(selectedPlant)}`">
                  {{ getDifficultyIcon(selectedPlant) }} {{ selectedPlant.difficulty }}
                </span>
              </div>
            </div>
            
            <div class="detail-section">
              <h3>📝 Informations</h3>
              <p class="no-info">Informations détaillées bientôt disponibles...</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useIndoorPlantsStore } from '../stores/indoorPlants'
import BaseForm from '@/components/BaseForm.vue'
import type { IndoorPlant } from '@/types'

const store = useIndoorPlantsStore()
const plants = computed(() => store.plants)
const showAddForm = ref(false)
const editingPlant = ref<IndoorPlant | null>(null)
const selectedPlant = ref<IndoorPlant | null>(null)
const searchQuery = ref('')
const activeFilters = ref<string[]>([])
const viewMode = ref<'grid' | 'list'>('grid')

const form = ref({ 
  name: '', 
  species: '',
  family: '',
  difficulty: ''
})

// Filtres rapides
const quickFilters = [
  { key: 'easy', label: 'Facile', icon: '🌱' },
  { key: 'medium', label: 'Modéré', icon: '🌿' },
  { key: 'hard', label: 'Difficile', icon: '🏆' },
  { key: 'flowering', label: 'Fleuries', icon: '🌸' }
]

// Champs du formulaire
const plantFields = [
  {
    name: 'name',
    label: 'Nom de la plante',
    type: 'text',
    required: true,
    placeholder: 'Ex: Monstera deliciosa'
  },
  {
    name: 'species',
    label: 'Nom scientifique',
    type: 'text',
    required: true,
    placeholder: 'Ex: Monstera deliciosa'
  },
  {
    name: 'family',
    label: 'Famille',
    type: 'text',
    placeholder: 'Ex: Araceae'
  },
  {
    name: 'difficulty',
    label: 'Niveau de difficulté',
    type: 'select',
    options: [
      { value: '', label: 'Non spécifié' },
      { value: 'Facile', label: '🌱 Facile' },
      { value: 'Modéré', label: '🌿 Modéré' },
      { value: 'Difficile', label: '🏆 Difficile' }
    ]
  }
]

// Computed properties pour les statistiques
const filteredPlants = computed(() => {
  let result = plants.value

  // Filtrage par recherche
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(plant => 
      plant.name?.toLowerCase().includes(query) ||
      plant.species?.toLowerCase().includes(query) ||
      plant.family?.toLowerCase().includes(query) ||
      plant.difficulty?.toLowerCase().includes(query)
    )
  }

  // Filtrage par filtres actifs
  if (activeFilters.value.length > 0) {
    result = result.filter(plant => {
      return activeFilters.value.some(filter => {
        switch (filter) {
          case 'easy':
            return plant.difficulty?.toLowerCase() === 'facile'
          case 'medium':
            return plant.difficulty?.toLowerCase() === 'modéré'
          case 'hard':
            return plant.difficulty?.toLowerCase() === 'difficile'
          case 'flowering':
            // Pour l'instant, on ne peut pas filtrer par plantes fleuries
            // car cette info n'est pas dans le modèle
            return false
          default:
            return false
        }
      })
    })
  }

  return result
})

const easyPlants = computed(() => 
  plants.value.filter(p => p.difficulty?.toLowerCase() === 'facile')
)

const challengingPlants = computed(() => 
  plants.value.filter(p => p.difficulty?.toLowerCase() === 'difficile')
)

// Méthodes
onMounted(() => {
  store.fetchPlants()
})

const onSearchInput = () => {
  // Debounce la recherche si nécessaire
}

const clearSearch = () => {
  searchQuery.value = ''
}

const toggleFilter = (filterKey: string) => {
  const index = activeFilters.value.indexOf(filterKey)
  if (index > -1) {
    activeFilters.value.splice(index, 1)
  } else {
    activeFilters.value.push(filterKey)
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  activeFilters.value = []
}

const getDifficultyLevel = (plant: IndoorPlant): string => {
  if (!plant.difficulty) return 'unknown'
  const difficulty = plant.difficulty.toLowerCase()
  if (difficulty === 'facile') return 'easy'
  if (difficulty === 'modéré') return 'medium'
  if (difficulty === 'difficile') return 'hard'
  return 'unknown'
}

const getDifficultyIcon = (plant: IndoorPlant): string => {
  const level = getDifficultyLevel(plant)
  switch (level) {
    case 'easy': return '🌱'
    case 'medium': return '🌿'
    case 'hard': return '🏆'
    default: return '❓'
  }
}

const viewPlantDetails = (plant: IndoorPlant) => {
  selectedPlant.value = plant
}

const closeDetails = () => {
  selectedPlant.value = null
}

const editPlant = (plant: IndoorPlant) => {
  editingPlant.value = plant
  form.value = { 
    name: plant.name || '', 
    species: plant.species || '',
    family: (plant as any).family || '',
    difficulty: (plant as any).difficulty || ''
  }
  showAddForm.value = false
}

const deletePlant = async (id: number) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cette espèce du catalogue ?')) {
    await store.deletePlant(id)
  }
}

const submitForm = async (formData: Record<string, any>) => {
  try {
    if (editingPlant.value) {
      await store.updatePlant(editingPlant.value.id, formData)
      editingPlant.value = null
    } else {
      const plantData = {
        name: formData.name as string,
        species: formData.species as string,
        family: formData.family as string,
        difficulty: formData.difficulty as string
      }
      await store.addPlant(plantData)
    }
    closeForm()
  } catch (error) {
    console.error('Erreur lors de la soumission:', error)
  }
}

const closeForm = () => {
  editingPlant.value = null
  showAddForm.value = false
  form.value = { name: '', species: '', family: '', difficulty: '' }
}
</script>

<style scoped>
/* === Layout principal === */
.indoor-plants-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  background: #f8fafc;
  min-height: 100vh;
}

/* === En-tête de page === */
.page-header {
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2.5rem;
  border-radius: 16px;
  color: white;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.header-text h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-text p {
  margin: 0;
  font-size: 1.125rem;
  opacity: 0.9;
  max-width: 600px;
}

/* === Section de recherche === */
.search-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.search-bar {
  margin-bottom: 1rem;
}

.search-input-group {
  position: relative;
  max-width: 500px;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.125rem;
  color: #64748b;
}

.search-input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  border: 2px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #f8fafc;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.clear-search-btn {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: #e2e8f0;
  border: none;
  border-radius: 6px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.75rem;
  color: #64748b;
  transition: all 0.2s ease;
}

.clear-search-btn:hover {
  background: #cbd5e1;
  color: #475569;
}

/* === Filtres rapides === */
.quick-filters {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.filter-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: 2px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
}

.filter-btn:hover {
  border-color: #cbd5e1;
  background: #f8fafc;
}

.filter-btn.active {
  border-color: #667eea;
  background: #667eea;
  color: white;
}

.filter-icon {
  font-size: 1rem;
}

/* === Statistiques === */
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
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 2rem;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 10px;
}

.stat-content h3 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  color: #1e293b;
}

.stat-content p {
  margin: 0;
  color: #64748b;
  font-weight: 500;
}

/* === Messages d'état === */
.error-message {
  background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
  color: #dc2626;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  border-left: 4px solid #dc2626;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 500;
}

.error-icon {
  font-size: 1.25rem;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top: 3px solid #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* === En-tête du catalogue === */
.catalog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.catalog-header h2 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 600;
}

.view-controls {
  display: flex;
  gap: 0.25rem;
  background: white;
  padding: 0.25rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.view-btn {
  padding: 0.5rem;
  border: none;
  background: transparent;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.125rem;
  color: #64748b;
  transition: all 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.view-btn:hover {
  background: #f1f5f9;
  color: #475569;
}

.view-btn.active {
  background: #667eea;
  color: white;
}

/* === Grille des plantes === */
.plants-grid {
  display: grid;
  gap: 1.5rem;
}

.plants-grid.grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}

.plants-grid.list {
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* === Cartes de plantes === */
.plant-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.plant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.plant-card.list {
  display: flex;
  align-items: center;
  padding: 1rem;
}

.plant-card.grid .plant-image {
  height: 180px;
}

.plant-card.list .plant-image {
  width: 80px;
  height: 80px;
  margin-right: 1rem;
  flex-shrink: 0;
}

.plant-image {
  position: relative;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.plant-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  text-align: center;
}

.placeholder-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.plant-card.list .placeholder-icon {
  font-size: 1.5rem;
  margin-bottom: 0;
}

.difficulty-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.difficulty-easy {
  background: rgba(34, 197, 94, 0.9);
}

.difficulty-medium {
  background: rgba(251, 191, 36, 0.9);
}

.difficulty-hard {
  background: rgba(239, 68, 68, 0.9);
}

.difficulty-unknown {
  background: rgba(107, 114, 128, 0.9);
}

/* === Informations de la plante === */
.plant-info {
  padding: 1.5rem;
}

.plant-card.list .plant-info {
  padding: 0;
  flex: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.plant-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
}

.plant-card.list .plant-name {
  margin-bottom: 0.25rem;
  font-size: 1rem;
}

.plant-scientific {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  color: #64748b;
  font-style: italic;
  line-height: 1.4;
}

.plant-card.list .plant-scientific {
  margin-bottom: 0;
  font-size: 0.8rem;
}

.plant-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.plant-card.list .plant-meta {
  margin-bottom: 0;
  margin-right: 1rem;
}

.meta-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #64748b;
  background: #f8fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-weight: 500;
  border: 1px solid #e2e8f0;
}

.meta-tag.difficulty {
  background: #f0f9ff;
  color: #0369a1;
  border-color: #bae6fd;
}

.meta-icon {
  font-size: 0.875rem;
}

/* === Actions des plantes === */
.plant-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.5rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 36px;
  height: 36px;
}

.plant-card.list .action-btn {
  padding: 0.5rem 0.75rem;
}

.action-btn--primary {
  background: #3b82f6;
  color: white;
}

.action-btn--primary:hover {
  background: #2563eb;
  transform: translateY(-1px);
}

.action-btn--secondary {
  background: #6b7280;
  color: white;
}

.action-btn--secondary:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

.action-btn--danger {
  background: #ef4444;
  color: white;
}

.action-btn--danger:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 1rem;
}

/* === État vide === */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.75rem 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 600;
}

.empty-state p {
  margin: 0 0 2rem 0;
  color: #64748b;
  line-height: 1.6;
}

.empty-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* === Boutons === */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  font-size: 1rem;
  line-height: 1;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: #6b7280;
  color: white;
}

.btn-secondary:hover {
  background: #4b5563;
  transform: translateY(-1px);
}

/* === Modales === */
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
  backdrop-filter: blur(4px);
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.modal-content--large {
  max-width: 800px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background: #f8fafc;
  border-radius: 12px 12px 0 0;
}

.modal-header h2 {
  margin: 0;
  color: #1e293b;
  font-size: 1.5rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.modal-icon {
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #64748b;
  transition: color 0.2s ease;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}

.close-btn:hover {
  color: #1e293b;
  background: #f1f5f9;
}

/* === Détails de la plante === */
.plant-details {
  padding: 1.5rem;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
}

.details-image {
  display: flex;
  justify-content: center;
}

.plant-placeholder.large {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border: 2px dashed #cbd5e1;
}

.plant-placeholder.large .placeholder-icon {
  font-size: 3rem;
}

.plant-placeholder.large p {
  margin-top: 0.5rem;
  font-size: 0.875rem;
  color: #64748b;
}

.details-info {
  space-y: 1.5rem;
}

.detail-section {
  margin-bottom: 1.5rem;
}

.detail-section h3 {
  margin: 0 0 1rem 0;
  color: #1e293b;
  font-size: 1.125rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detail-grid {
  display: grid;
  gap: 0.75rem;
}

.detail-item {
  display: grid;
  grid-template-columns: 140px 1fr;
  gap: 0.75rem;
  align-items: center;
}

.detail-item strong {
  color: #475569;
  font-weight: 500;
}

.detail-item span {
  color: #1e293b;
}

.difficulty-info {
  display: flex;
  align-items: center;
}

.difficulty-badge.large {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: auto;
  height: auto;
}

.no-info {
  color: #64748b;
  font-style: italic;
  margin: 0;
}

/* === Actions de formulaire === */
.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

/* === Responsive === */
@media (max-width: 768px) {
  .indoor-plants-page {
    padding: 1rem;
  }

  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 1.5rem;
  }

  .header-text h1 {
    font-size: 2rem;
  }

  .plants-grid.grid {
    grid-template-columns: 1fr;
  }

  .plant-card.list {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .plant-card.list .plant-image {
    width: 100%;
    height: 120px;
    margin-right: 0;
  }

  .plant-card.list .plant-info {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }

  .catalog-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .quick-filters {
    justify-content: center;
  }

  .plant-details {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .empty-actions {
    flex-direction: column;
    align-items: center;
  }
}

@media (max-width: 480px) {
  .search-input-group {
    max-width: none;
  }

  .btn {
    padding: 0.625rem 1.25rem;
    font-size: 0.875rem;
  }

  .modal-content {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
}
</style>
