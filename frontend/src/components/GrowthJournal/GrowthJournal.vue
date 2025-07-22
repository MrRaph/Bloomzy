<template>
  <div class="growth-journal">
    <div class="growth-journal-header">
      <h2>Journal de Croissance</h2>
      <div class="header-actions">
        <select v-model="selectedType" class="filter-select" @change="loadEntries">
          <option value="">Tous les types</option>
          <option value="photo">Photos</option>
          <option value="measurement">Mesures</option>
          <option value="observation">Observations</option>
        </select>
        <button @click="showCreateModal = true" class="btn-primary">
          Nouvelle entrée
        </button>
      </div>
    </div>

    <div class="growth-journal-tabs">
      <button 
        :class="['tab', { active: activeTab === 'entries' }]" 
        @click="activeTab = 'entries'"
      >
        Entrées ({{ entries.length }})
      </button>
      <button 
        :class="['tab', { active: activeTab === 'analytics' }]" 
        @click="activeTab = 'analytics'; loadAnalytics()"
      >
        Analyses
      </button>
      <button 
        :class="['tab', { active: activeTab === 'comparison' }]" 
        @click="activeTab = 'comparison'; loadComparison()"
      >
        Comparaison
      </button>
    </div>

    <div class="growth-journal-content">
      <!-- Entries Tab -->
      <div v-if="activeTab === 'entries'" class="entries-tab">
        <div v-if="loading" class="loading">
          Chargement des entrées...
        </div>
        <div v-else-if="entries.length === 0" class="empty-state">
          <p>Aucune entrée trouvée pour cette plante.</p>
          <button @click="showCreateModal = true" class="btn-primary">
            Créer la première entrée
          </button>
        </div>
        <div v-else class="entries-list">
          <GrowthEntryCard
            v-for="entry in entries"
            :key="entry.id"
            :entry="entry"
            @edit="editEntry"
            @delete="deleteEntry"
          />
        </div>
      </div>

      <!-- Analytics Tab -->
      <div v-if="activeTab === 'analytics'" class="analytics-tab">
        <GrowthAnalytics 
          v-if="analytics"
          :analytics="analytics"
          :loading="analyticsLoading"
        />
      </div>

      <!-- Comparison Tab -->
      <div v-if="activeTab === 'comparison'" class="comparison-tab">
        <GrowthComparison
          v-if="comparison"
          :comparison="comparison"
          :loading="comparisonLoading"
        />
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <GrowthEntryModal
      v-if="showCreateModal || editingEntry"
      :entry="editingEntry"
      :plant-id="plantId"
      @close="closeModal"
      @success="onEntrySuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { GrowthEntry, GrowthAnalytics as GrowthAnalyticsType, GrowthComparison as GrowthComparisonType } from '@/types'
import { growthJournalApi } from '@/services/api'
import { useNotifications } from '@/composables/useNotifications'
import GrowthEntryCard from './GrowthEntryCard.vue'
import GrowthEntryModal from './GrowthEntryModal.vue'
import GrowthAnalytics from './GrowthAnalytics.vue'
import GrowthComparison from './GrowthComparison.vue'

const props = defineProps<{
  plantId: number
}>()

const { addNotification } = useNotifications()

const activeTab = ref('entries')
const selectedType = ref('')
const loading = ref(false)
const analyticsLoading = ref(false)
const comparisonLoading = ref(false)
const showCreateModal = ref(false)
const editingEntry = ref<GrowthEntry | null>(null)

const entries = ref<GrowthEntry[]>([])
const analytics = ref<GrowthAnalyticsType | null>(null)
const comparison = ref<GrowthComparisonType | null>(null)

const loadEntries = async () => {
  loading.value = true
  try {
    const params = selectedType.value ? { type: selectedType.value } : {}
    const response = await growthJournalApi.list(props.plantId, params)
    entries.value = response.data || []
  } catch (error) {
    addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des entrées'
    })
  } finally {
    loading.value = false
  }
}

const loadAnalytics = async () => {
  if (analytics.value) return // Already loaded
  
  analyticsLoading.value = true
  try {
    const response = await growthJournalApi.getAnalytics(props.plantId)
    analytics.value = response.data || null
  } catch (error) {
    addNotification({
      type: 'error',
      message: 'Erreur lors du chargement des analyses'
    })
  } finally {
    analyticsLoading.value = false
  }
}

const loadComparison = async () => {
  if (comparison.value) return // Already loaded
  
  comparisonLoading.value = true
  try {
    const response = await growthJournalApi.getComparison(props.plantId)
    comparison.value = response.data || null
  } catch (error) {
    addNotification({
      type: 'error',
      message: 'Erreur lors du chargement de la comparaison'
    })
  } finally {
    comparisonLoading.value = false
  }
}

const editEntry = (entry: GrowthEntry) => {
  editingEntry.value = entry
}

const deleteEntry = async (entry: GrowthEntry) => {
  if (!confirm('Êtes-vous sûr de vouloir supprimer cette entrée ?')) {
    return
  }
  
  try {
    await growthJournalApi.delete(props.plantId, entry.id)
    await loadEntries() // Reload entries
    addNotification({
      type: 'success',
      message: 'Entrée supprimée avec succès'
    })
  } catch (error) {
    addNotification({
      type: 'error',
      message: 'Erreur lors de la suppression'
    })
  }
}

const closeModal = () => {
  showCreateModal.value = false
  editingEntry.value = null
}

const onEntrySuccess = () => {
  closeModal()
  loadEntries()
  // Reset analytics and comparison to force reload
  analytics.value = null
  comparison.value = null
}

onMounted(() => {
  loadEntries()
})
</script>

<style scoped>
.growth-journal {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.growth-journal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.growth-journal-header h2 {
  color: #2d5a27;
  font-size: 28px;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 15px;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: white;
  color: #333;
  font-size: 14px;
}

.btn-primary {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background: #45a049;
}

.growth-journal-tabs {
  display: flex;
  border-bottom: 2px solid #e0e0e0;
  margin-bottom: 30px;
}

.tab {
  background: none;
  border: none;
  padding: 12px 24px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  color: #666;
  transition: all 0.2s;
  border-bottom: 3px solid transparent;
}

.tab:hover {
  color: #4CAF50;
}

.tab.active {
  color: #4CAF50;
  border-bottom-color: #4CAF50;
}

.growth-journal-content {
  min-height: 400px;
}

.loading {
  text-align: center;
  padding: 50px;
  color: #666;
  font-size: 16px;
}

.empty-state {
  text-align: center;
  padding: 50px;
}

.empty-state p {
  color: #666;
  font-size: 16px;
  margin-bottom: 20px;
}

.entries-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}
</style>