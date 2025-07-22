<template>
  <div class="growth-comparison">
    <div v-if="loading" class="loading">
      Chargement de la comparaison...
    </div>
    
    <div v-else-if="!comparison || (!comparison.first_entry && !comparison.last_entry)" class="empty-state">
      <p>Pas assez de données pour effectuer une comparaison.</p>
      <p class="subtitle">Il faut au moins 2 entrées pour comparer l'évolution.</p>
    </div>

    <div v-else class="comparison-content">
      <!-- Comparison Header -->
      <div class="comparison-header">
        <h4>Comparaison sur {{ comparison.comparison_period_days }} jours</h4>
        <div class="date-range">
          <span v-if="comparison.first_entry">{{ formatDate(comparison.first_entry.entry_date) }}</span>
          <span class="arrow">→</span>
          <span v-if="comparison.last_entry">{{ formatDate(comparison.last_entry.entry_date) }}</span>
        </div>
      </div>

      <!-- Photo Comparison -->
      <div v-if="comparison.photo_comparison && (comparison.photo_comparison.first_photo || comparison.photo_comparison.last_photo)" class="photo-comparison">
        <h5>📸 Évolution visuelle</h5>
        <div class="photos-container">
          <div class="photo-before">
            <div class="photo-label">Avant</div>
            <div v-if="comparison.photo_comparison.first_photo" class="photo-frame">
              <img :src="comparison.photo_comparison.first_photo" alt="Photo avant" />
            </div>
            <div v-else class="photo-placeholder">
              Pas de photo disponible
            </div>
          </div>
          
          <div class="comparison-arrow">
            <span class="arrow-icon">→</span>
          </div>
          
          <div class="photo-after">
            <div class="photo-label">Après</div>
            <div v-if="comparison.photo_comparison.last_photo" class="photo-frame">
              <img :src="comparison.photo_comparison.last_photo" alt="Photo après" />
            </div>
            <div v-else class="photo-placeholder">
              Pas de photo disponible
            </div>
          </div>
        </div>
      </div>

      <!-- Measurements Comparison -->
      <div class="measurements-comparison">
        <h5>📏 Évolution des mesures</h5>
        
        <div v-if="hasChanges" class="changes-grid">
          <div v-if="comparison.changes.height_cm !== undefined" class="change-item">
            <div class="change-label">
              <span class="icon">📏</span>
              Hauteur
            </div>
            <div class="change-values">
              <span class="before">{{ getBeforeValue('height_cm') }} cm</span>
              <span class="arrow">→</span>
              <span class="after">{{ getAfterValue('height_cm') }} cm</span>
            </div>
            <div :class="['change-indicator', getChangeClass(comparison.changes.height_cm)]">
              {{ formatChange(comparison.changes.height_cm, 'cm') }}
            </div>
          </div>

          <div v-if="comparison.changes.width_cm !== undefined" class="change-item">
            <div class="change-label">
              <span class="icon">↔️</span>
              Largeur
            </div>
            <div class="change-values">
              <span class="before">{{ getBeforeValue('width_cm') }} cm</span>
              <span class="arrow">→</span>
              <span class="after">{{ getAfterValue('width_cm') }} cm</span>
            </div>
            <div :class="['change-indicator', getChangeClass(comparison.changes.width_cm)]">
              {{ formatChange(comparison.changes.width_cm, 'cm') }}
            </div>
          </div>

          <div v-if="comparison.changes.leaf_count !== undefined" class="change-item">
            <div class="change-label">
              <span class="icon">🍃</span>
              Feuilles
            </div>
            <div class="change-values">
              <span class="before">{{ getBeforeValue('leaf_count') }}</span>
              <span class="arrow">→</span>
              <span class="after">{{ getAfterValue('leaf_count') }}</span>
            </div>
            <div :class="['change-indicator', getChangeClass(comparison.changes.leaf_count)]">
              {{ formatChange(comparison.changes.leaf_count, '') }}
            </div>
          </div>

          <div v-if="comparison.changes.ai_health_score !== undefined" class="change-item">
            <div class="change-label">
              <span class="icon">🤖</span>
              Score IA
            </div>
            <div class="change-values">
              <span class="before">{{ getBeforeValue('ai_health_score', true) }}/100</span>
              <span class="arrow">→</span>
              <span class="after">{{ getAfterValue('ai_health_score', true) }}/100</span>
            </div>
            <div :class="['change-indicator', getChangeClass(comparison.changes.ai_health_score)]">
              {{ formatChange(comparison.changes.ai_health_score, '') }}
            </div>
          </div>
        </div>

        <div v-else class="no-changes">
          <p>Aucune donnée de mesure comparable disponible.</p>
        </div>
      </div>

      <!-- Health Comparison -->
      <div v-if="hasHealthComparison" class="health-comparison">
        <h5>🌿 Évolution de la santé</h5>
        <div class="health-comparison-grid">
          <div class="health-before">
            <h6>Avant</h6>
            <div class="health-details">
              <div v-if="comparison.first_entry?.leaf_color" class="health-item">
                <span class="label">Couleur :</span>
                <span :class="['leaf-color', comparison.first_entry.leaf_color]">
                  {{ getLeafColorLabel(comparison.first_entry.leaf_color) }}
                </span>
              </div>
              <div v-if="comparison.first_entry?.stem_firmness" class="health-item">
                <span class="label">Fermeté :</span>
                <span>{{ getStemFirmnessLabel(comparison.first_entry.stem_firmness) }}</span>
              </div>
              <div v-if="comparison.first_entry?.has_flowers || comparison.first_entry?.has_fruits" class="health-item">
                <span class="label">Reproduction :</span>
                <span>
                  <span v-if="comparison.first_entry.has_flowers">🌸</span>
                  <span v-if="comparison.first_entry.has_fruits">🍓</span>
                  <span v-if="!comparison.first_entry.has_flowers && !comparison.first_entry.has_fruits">Aucune</span>
                </span>
              </div>
            </div>
          </div>

          <div class="health-after">
            <h6>Après</h6>
            <div class="health-details">
              <div v-if="comparison.last_entry?.leaf_color" class="health-item">
                <span class="label">Couleur :</span>
                <span :class="['leaf-color', comparison.last_entry.leaf_color]">
                  {{ getLeafColorLabel(comparison.last_entry.leaf_color) }}
                </span>
              </div>
              <div v-if="comparison.last_entry?.stem_firmness" class="health-item">
                <span class="label">Fermeté :</span>
                <span>{{ getStemFirmnessLabel(comparison.last_entry.stem_firmness) }}</span>
              </div>
              <div v-if="comparison.last_entry?.has_flowers || comparison.last_entry?.has_fruits" class="health-item">
                <span class="label">Reproduction :</span>
                <span>
                  <span v-if="comparison.last_entry.has_flowers">🌸</span>
                  <span v-if="comparison.last_entry.has_fruits">🍓</span>
                  <span v-if="!comparison.last_entry.has_flowers && !comparison.last_entry.has_fruits">Aucune</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Growth Summary -->
      <div class="growth-summary">
        <h5>📈 Résumé de l'évolution</h5>
        <div class="summary-content">
          <div class="summary-stats">
            <div class="stat">
              <span class="label">Période suivie :</span>
              <span class="value">{{ comparison.comparison_period_days }} jours</span>
            </div>
            <div v-if="hasPositiveGrowth" class="stat positive">
              <span class="label">Évolution :</span>
              <span class="value">Croissance positive détectée</span>
            </div>
            <div v-else-if="hasNegativeGrowth" class="stat negative">
              <span class="label">Évolution :</span>
              <span class="value">Décroissance détectée</span>
            </div>
            <div v-else class="stat neutral">
              <span class="label">Évolution :</span>
              <span class="value">Stabilité observée</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { GrowthComparison } from '@/types'

const props = defineProps<{
  comparison: GrowthComparison | null
  loading: boolean
}>()

const hasChanges = computed(() => {
  if (!props.comparison) return false
  return Object.keys(props.comparison.changes).length > 0
})

const hasHealthComparison = computed(() => {
  if (!props.comparison?.first_entry || !props.comparison?.last_entry) return false
  return (props.comparison.first_entry.leaf_color || props.comparison.first_entry.stem_firmness ||
          props.comparison.first_entry.has_flowers || props.comparison.first_entry.has_fruits) ||
         (props.comparison.last_entry.leaf_color || props.comparison.last_entry.stem_firmness ||
          props.comparison.last_entry.has_flowers || props.comparison.last_entry.has_fruits)
})

const hasPositiveGrowth = computed(() => {
  if (!props.comparison) return false
  return Object.values(props.comparison.changes).some(change => change > 0)
})

const hasNegativeGrowth = computed(() => {
  if (!props.comparison) return false
  return Object.values(props.comparison.changes).some(change => change < 0)
})

const getBeforeValue = (field: string, round = false): string => {
  const value = props.comparison?.first_entry?.[field as keyof typeof props.comparison.first_entry]
  if (value === undefined || value === null) return 'N/A'
  return round ? Math.round(Number(value)).toString() : value.toString()
}

const getAfterValue = (field: string, round = false): string => {
  const value = props.comparison?.last_entry?.[field as keyof typeof props.comparison.last_entry]
  if (value === undefined || value === null) return 'N/A'
  return round ? Math.round(Number(value)).toString() : value.toString()
}

const getChangeClass = (change: number): string => {
  if (change > 0) return 'positive'
  if (change < 0) return 'negative'
  return 'neutral'
}

const formatChange = (change: number, unit: string): string => {
  const sign = change > 0 ? '+' : ''
  return `${sign}${change}${unit}`
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

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  })
}
</script>

<style scoped>
.growth-comparison {
  max-width: 1000px;
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
  margin-bottom: 10px;
}

.subtitle {
  font-size: 14px !important;
  color: #999 !important;
}

.comparison-content {
  padding: 20px 0;
}

.comparison-header {
  text-align: center;
  margin-bottom: 30px;
}

.comparison-header h4 {
  color: #2d5a27;
  font-size: 24px;
  margin-bottom: 10px;
  font-weight: 600;
}

.date-range {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  color: #666;
  font-size: 16px;
}

.arrow {
  color: #4CAF50;
  font-weight: bold;
}

.photo-comparison,
.measurements-comparison,
.health-comparison,
.growth-summary {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
}

.photo-comparison h5,
.measurements-comparison h5,
.health-comparison h5,
.growth-summary h5 {
  color: #2d5a27;
  font-size: 18px;
  margin-bottom: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}

.photos-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 20px;
  align-items: center;
}

.photo-frame {
  width: 200px;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.photo-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  width: 200px;
  height: 200px;
  border: 2px dashed #ddd;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #999;
  font-style: italic;
}

.photo-label {
  text-align: center;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
  font-size: 16px;
}

.comparison-arrow {
  display: flex;
  justify-content: center;
}

.arrow-icon {
  font-size: 32px;
  color: #4CAF50;
  font-weight: bold;
}

.changes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.change-item {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
  border-left: 4px solid #4CAF50;
}

.change-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.icon {
  font-size: 18px;
}

.change-values {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 14px;
}

.before {
  color: #666;
}

.after {
  color: #333;
  font-weight: 600;
}

.change-values .arrow {
  color: #4CAF50;
  font-weight: bold;
}

.change-indicator {
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 14px;
  text-align: center;
}

.change-indicator.positive {
  background: #E8F5E8;
  color: #2E7D32;
}

.change-indicator.negative {
  background: #FFEBEE;
  color: #C62828;
}

.change-indicator.neutral {
  background: #F5F5F5;
  color: #666;
}

.no-changes {
  text-align: center;
  padding: 30px;
  color: #666;
}

.health-comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}

.health-before,
.health-after {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
}

.health-before h6,
.health-after h6 {
  color: #2d5a27;
  font-size: 16px;
  margin-bottom: 15px;
  text-align: center;
}

.health-details {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.health-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.health-item .label {
  color: #666;
  font-size: 14px;
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

.summary-content {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 10px;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 8px;
}

.stat.positive {
  border-left: 4px solid #4CAF50;
}

.stat.negative {
  border-left: 4px solid #F44336;
}

.stat.neutral {
  border-left: 4px solid #9E9E9E;
}

.stat .label {
  color: #666;
  font-weight: 500;
}

.stat .value {
  font-weight: 600;
  color: #333;
}

.stat.positive .value {
  color: #2E7D32;
}

.stat.negative .value {
  color: #C62828;
}
</style>