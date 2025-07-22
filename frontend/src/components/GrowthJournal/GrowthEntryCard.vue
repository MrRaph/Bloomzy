<template>
  <div class="growth-entry-card">
    <div class="entry-header">
      <div class="entry-type">
        <span :class="['type-badge', entry.entry_type]">
          {{ getTypeLabel(entry.entry_type) }}
        </span>
        <span class="entry-date">{{ formatDate(entry.entry_date) }}</span>
      </div>
      <div class="entry-actions">
        <button @click="$emit('edit', entry)" class="btn-edit">
          ✏️
        </button>
        <button @click="$emit('delete', entry)" class="btn-delete">
          🗑️
        </button>
      </div>
    </div>

    <div v-if="entry.photo_url" class="entry-photo">
      <img :src="entry.photo_url" :alt="entry.photo_description || 'Photo de croissance'" />
      <p v-if="entry.photo_description" class="photo-description">
        {{ entry.photo_description }}
      </p>
    </div>

    <div v-if="hasMeasurements" class="entry-measurements">
      <h4>Mesures</h4>
      <div class="measurements-grid">
        <div v-if="entry.height_cm" class="measurement">
          <span class="label">Hauteur :</span>
          <span class="value">{{ entry.height_cm }} cm</span>
        </div>
        <div v-if="entry.width_cm" class="measurement">
          <span class="label">Largeur :</span>
          <span class="value">{{ entry.width_cm }} cm</span>
        </div>
        <div v-if="entry.leaf_count" class="measurement">
          <span class="label">Feuilles :</span>
          <span class="value">{{ entry.leaf_count }}</span>
        </div>
        <div v-if="entry.stem_count" class="measurement">
          <span class="label">Tiges :</span>
          <span class="value">{{ entry.stem_count }}</span>
        </div>
      </div>
    </div>

    <div v-if="hasHealthInfo" class="entry-health">
      <h4>État de santé</h4>
      <div class="health-info">
        <div v-if="entry.leaf_color" class="health-item">
          <span class="label">Couleur des feuilles :</span>
          <span :class="['leaf-color', entry.leaf_color]">{{ getLeafColorLabel(entry.leaf_color) }}</span>
        </div>
        <div v-if="entry.stem_firmness" class="health-item">
          <span class="label">Fermeté des tiges :</span>
          <span class="value">{{ getStemFirmnessLabel(entry.stem_firmness) }}</span>
        </div>
        <div v-if="entry.has_flowers || entry.has_fruits" class="health-item">
          <span class="label">Reproduction :</span>
          <span class="value">
            <span v-if="entry.has_flowers">🌸 Fleurs</span>
            <span v-if="entry.has_flowers && entry.has_fruits"> • </span>
            <span v-if="entry.has_fruits">🍓 Fruits</span>
          </span>
        </div>
        <div v-if="entry.ai_health_score" class="health-item">
          <span class="label">Score IA :</span>
          <span :class="['ai-score', getHealthScoreClass(entry.ai_health_score)]">
            {{ Math.round(entry.ai_health_score) }}/100
          </span>
        </div>
      </div>
    </div>

    <div v-if="hasNotes" class="entry-notes">
      <div v-if="entry.health_notes" class="note-section">
        <h5>Notes de santé :</h5>
        <p>{{ entry.health_notes }}</p>
      </div>
      <div v-if="entry.growth_notes" class="note-section">
        <h5>Notes de croissance :</h5>
        <p>{{ entry.growth_notes }}</p>
      </div>
      <div v-if="entry.user_observations" class="note-section">
        <h5>Observations :</h5>
        <p>{{ entry.user_observations }}</p>
      </div>
      <div v-if="entry.ai_growth_analysis" class="note-section">
        <h5>Analyse IA :</h5>
        <p>{{ entry.ai_growth_analysis }}</p>
      </div>
      <div v-if="entry.ai_recommendations" class="note-section">
        <h5>Recommandations IA :</h5>
        <p>{{ entry.ai_recommendations }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { GrowthEntry } from '@/types'

const props = defineProps<{
  entry: GrowthEntry
}>()

defineEmits<{
  edit: [entry: GrowthEntry]
  delete: [entry: GrowthEntry]
}>()

const hasMeasurements = computed(() => {
  return props.entry.height_cm || props.entry.width_cm || props.entry.leaf_count || props.entry.stem_count
})

const hasHealthInfo = computed(() => {
  return props.entry.leaf_color || props.entry.stem_firmness || props.entry.has_flowers || 
         props.entry.has_fruits || props.entry.ai_health_score
})

const hasNotes = computed(() => {
  return props.entry.health_notes || props.entry.growth_notes || props.entry.user_observations ||
         props.entry.ai_growth_analysis || props.entry.ai_recommendations
})

const getTypeLabel = (type: string): string => {
  const labels = {
    photo: 'Photo',
    measurement: 'Mesure',
    observation: 'Observation'
  }
  return labels[type as keyof typeof labels] || type
}

const getLeafColorLabel = (color: string): string => {
  const labels = {
    green: 'Vert',
    yellow: 'Jaune',
    brown: 'Marron',
    red: 'Rouge',
    purple: 'Violet',
    variegated: 'Panaché'
  }
  return labels[color as keyof typeof labels] || color
}

const getStemFirmnessLabel = (firmness: string): string => {
  const labels = {
    firm: 'Ferme',
    soft: 'Souple',
    brittle: 'Cassant'
  }
  return labels[firmness as keyof typeof labels] || firmness
}

const getHealthScoreClass = (score: number): string => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'fair'
  return 'poor'
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}
</script>

<style scoped>
.growth-entry-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.growth-entry-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.entry-type {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.type-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.type-badge.photo {
  background: #E3F2FD;
  color: #1976D2;
}

.type-badge.measurement {
  background: #E8F5E8;
  color: #388E3C;
}

.type-badge.observation {
  background: #FFF3E0;
  color: #F57C00;
}

.entry-date {
  color: #666;
  font-size: 14px;
}

.entry-actions {
  display: flex;
  gap: 5px;
}

.btn-edit,
.btn-delete {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.btn-edit:hover {
  background: #f0f0f0;
}

.btn-delete:hover {
  background: #ffebee;
}

.entry-photo {
  margin-bottom: 15px;
}

.entry-photo img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
}

.photo-description {
  margin-top: 8px;
  color: #666;
  font-style: italic;
  font-size: 14px;
}

.entry-measurements,
.entry-health,
.entry-notes {
  margin-bottom: 15px;
}

.entry-measurements h4,
.entry-health h4 {
  color: #2d5a27;
  font-size: 16px;
  margin-bottom: 10px;
}

.measurements-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.measurement,
.health-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.label {
  color: #666;
  font-size: 14px;
}

.value {
  font-weight: 500;
  color: #333;
}

.leaf-color {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.leaf-color.green { background: #E8F5E8; color: #388E3C; }
.leaf-color.yellow { background: #FFFDE7; color: #F9A825; }
.leaf-color.brown { background: #EFEBE9; color: #6D4C41; }
.leaf-color.red { background: #FFEBEE; color: #D32F2F; }
.leaf-color.purple { background: #F3E5F5; color: #7B1FA2; }
.leaf-color.variegated { background: #F5F5F5; color: #424242; }

.ai-score {
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}

.ai-score.excellent { background: #E8F5E8; color: #2E7D32; }
.ai-score.good { background: #E3F2FD; color: #1976D2; }
.ai-score.fair { background: #FFF8E1; color: #F57C00; }
.ai-score.poor { background: #FFEBEE; color: #D32F2F; }

.health-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.note-section {
  margin-bottom: 12px;
}

.note-section:last-child {
  margin-bottom: 0;
}

.note-section h5 {
  color: #2d5a27;
  font-size: 14px;
  margin-bottom: 5px;
}

.note-section p {
  color: #555;
  font-size: 14px;
  line-height: 1.4;
  margin: 0;
}
</style>