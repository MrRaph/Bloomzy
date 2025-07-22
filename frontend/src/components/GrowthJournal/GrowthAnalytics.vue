<template>
  <div class="growth-analytics">
    <div v-if="loading" class="loading">
      Chargement des analyses...
    </div>
    
    <div v-else-if="!analytics || analytics.total_entries === 0" class="empty-state">
      <p>Aucune donnée disponible pour l'analyse.</p>
      <p class="subtitle">Ajoutez des entrées pour voir les tendances de croissance.</p>
    </div>

    <div v-else class="analytics-content">
      <!-- Summary Stats -->
      <div class="stats-overview">
        <div class="stat-card">
          <div class="stat-value">{{ analytics.total_entries }}</div>
          <div class="stat-label">Entrées totales</div>
        </div>
        <div class="stat-card">
          <div class="stat-value">{{ formatDateRange }}</div>
          <div class="stat-label">Période suivie</div>
        </div>
        <div class="stat-card" v-if="analytics.growth_rates">
          <div class="stat-value">{{ analytics.growth_rates.height_cm_per_day.toFixed(2) }} cm/j</div>
          <div class="stat-label">Croissance moyenne</div>
        </div>
      </div>

      <!-- Entry Types Distribution -->
      <div class="analytics-section">
        <h4>Répartition des types d'entrées</h4>
        <div class="entry-types">
          <div 
            v-for="(count, type) in analytics.entry_types" 
            :key="type"
            class="entry-type-item"
          >
            <span :class="['type-badge', type]">{{ getTypeLabel(type) }}</span>
            <span class="count">{{ count }}</span>
          </div>
        </div>
      </div>

      <!-- Growth Trends Charts -->
      <div v-if="hasGrowthData" class="analytics-section">
        <h4>Tendances de croissance</h4>
        
        <div v-if="analytics.growth_trends.height.length > 0" class="chart-container">
          <h5>Évolution de la hauteur</h5>
          <div class="simple-chart">
            <div 
              v-for="(point, index) in analytics.growth_trends.height" 
              :key="index"
              class="chart-point"
              :style="{ 
                left: `${(index / (analytics.growth_trends.height.length - 1)) * 100}%`,
                bottom: `${(point[1] / maxHeight) * 80 + 10}%`
              }"
              :title="`${formatChartDate(point[0])}: ${point[1]}cm`"
            >
              <div class="point-dot"></div>
              <div class="point-label">{{ point[1] }}cm</div>
            </div>
            <div class="chart-axis">
              <div class="axis-label">{{ formatChartDate(analytics.growth_trends.height[0]?.[0]) }}</div>
              <div class="axis-label">{{ formatChartDate(analytics.growth_trends.height[analytics.growth_trends.height.length - 1]?.[0]) }}</div>
            </div>
          </div>
        </div>

        <div v-if="analytics.growth_trends.width.length > 0" class="chart-container">
          <h5>Évolution de la largeur</h5>
          <div class="simple-chart">
            <div 
              v-for="(point, index) in analytics.growth_trends.width" 
              :key="index"
              class="chart-point"
              :style="{ 
                left: `${(index / (analytics.growth_trends.width.length - 1)) * 100}%`,
                bottom: `${(point[1] / maxWidth) * 80 + 10}%`
              }"
              :title="`${formatChartDate(point[0])}: ${point[1]}cm`"
            >
              <div class="point-dot"></div>
              <div class="point-label">{{ point[1] }}cm</div>
            </div>
          </div>
        </div>

        <div v-if="analytics.growth_trends.leaf_count.length > 0" class="chart-container">
          <h5>Évolution du nombre de feuilles</h5>
          <div class="simple-chart">
            <div 
              v-for="(point, index) in analytics.growth_trends.leaf_count" 
              :key="index"
              class="chart-point"
              :style="{ 
                left: `${(index / (analytics.growth_trends.leaf_count.length - 1)) * 100}%`,
                bottom: `${(point[1] / maxLeafCount) * 80 + 10}%`
              }"
              :title="`${formatChartDate(point[0])}: ${point[1]} feuilles`"
            >
              <div class="point-dot"></div>
              <div class="point-label">{{ point[1] }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Health Trends -->
      <div v-if="hasHealthData" class="analytics-section">
        <h4>Tendances de santé</h4>

        <div v-if="analytics.health_trends.ai_health_scores.length > 0" class="chart-container">
          <h5>Évolution du score de santé IA</h5>
          <div class="simple-chart">
            <div 
              v-for="(point, index) in analytics.health_trends.ai_health_scores" 
              :key="index"
              class="chart-point"
              :style="{ 
                left: `${(index / (analytics.health_trends.ai_health_scores.length - 1)) * 100}%`,
                bottom: `${(point[1] / 100) * 80 + 10}%`
              }"
              :title="`${formatChartDate(point[0])}: ${point[1]}/100`"
            >
              <div class="point-dot health-score"></div>
              <div class="point-label">{{ Math.round(point[1]) }}</div>
            </div>
          </div>
        </div>

        <div v-if="Object.keys(analytics.health_trends.leaf_color_distribution).length > 0" class="color-distribution">
          <h5>Répartition des couleurs de feuilles</h5>
          <div class="color-bars">
            <div 
              v-for="(count, color) in analytics.health_trends.leaf_color_distribution" 
              :key="color"
              class="color-bar"
            >
              <div 
                :class="['color-indicator', color]"
                :style="{ width: `${(count / maxColorCount) * 100}%` }"
              ></div>
              <span class="color-label">{{ getLeafColorLabel(color) }} ({{ count }})</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Growth Rate Summary -->
      <div v-if="analytics.growth_rates" class="analytics-section">
        <h4>Résumé de croissance</h4>
        <div class="growth-summary">
          <div class="summary-item">
            <span class="label">Croissance totale :</span>
            <span class="value">{{ analytics.growth_rates.total_growth_cm }} cm</span>
          </div>
          <div class="summary-item">
            <span class="label">Période de suivi :</span>
            <span class="value">{{ analytics.growth_rates.growth_period_days }} jours</span>
          </div>
          <div class="summary-item">
            <span class="label">Vitesse de croissance :</span>
            <span class="value">{{ analytics.growth_rates.height_cm_per_day.toFixed(3) }} cm/jour</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { GrowthAnalytics } from '@/types'

const props = defineProps<{
  analytics: GrowthAnalytics | null
  loading: boolean
}>()

const formatDateRange = computed(() => {
  if (!props.analytics?.date_range) return 'N/A'
  const start = new Date(props.analytics.date_range.start).toLocaleDateString('fr-FR')
  const end = new Date(props.analytics.date_range.end).toLocaleDateString('fr-FR')
  return `${start} - ${end}`
})

const hasGrowthData = computed(() => {
  if (!props.analytics) return false
  return props.analytics.growth_trends.height.length > 0 ||
         props.analytics.growth_trends.width.length > 0 ||
         props.analytics.growth_trends.leaf_count.length > 0
})

const hasHealthData = computed(() => {
  if (!props.analytics) return false
  return props.analytics.health_trends.ai_health_scores.length > 0 ||
         Object.keys(props.analytics.health_trends.leaf_color_distribution).length > 0
})

const maxHeight = computed(() => {
  if (!props.analytics?.growth_trends.height.length) return 100
  return Math.max(...props.analytics.growth_trends.height.map(p => p[1]))
})

const maxWidth = computed(() => {
  if (!props.analytics?.growth_trends.width.length) return 100
  return Math.max(...props.analytics.growth_trends.width.map(p => p[1]))
})

const maxLeafCount = computed(() => {
  if (!props.analytics?.growth_trends.leaf_count.length) return 100
  return Math.max(...props.analytics.growth_trends.leaf_count.map(p => p[1]))
})

const maxColorCount = computed(() => {
  if (!props.analytics?.health_trends.leaf_color_distribution) return 1
  return Math.max(...Object.values(props.analytics.health_trends.leaf_color_distribution))
})

const getTypeLabel = (type: string): string => {
  const labels = {
    photo: 'Photos',
    measurement: 'Mesures',
    observation: 'Observations'
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

const formatChartDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('fr-FR', {
    day: 'numeric',
    month: 'short'
  })
}
</script>

<style scoped>
.growth-analytics {
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

.analytics-content {
  padding: 20px 0;
}

.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #2d5a27;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.analytics-section {
  background: white;
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.analytics-section h4 {
  color: #2d5a27;
  font-size: 20px;
  margin-bottom: 20px;
  font-weight: 600;
}

.entry-types {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.entry-type-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
  background: #f9f9f9;
  border-radius: 8px;
}

.type-badge {
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

.count {
  font-weight: 600;
  color: #333;
}

.chart-container {
  margin-bottom: 30px;
}

.chart-container h5 {
  color: #2d5a27;
  font-size: 16px;
  margin-bottom: 15px;
}

.simple-chart {
  position: relative;
  height: 120px;
  background: #f9f9f9;
  border-radius: 8px;
  margin: 10px 0;
  border: 1px solid #eee;
}

.chart-point {
  position: absolute;
  transform: translateX(-50%);
}

.point-dot {
  width: 8px;
  height: 8px;
  background: #4CAF50;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.point-dot.health-score {
  background: #2196F3;
}

.point-label {
  position: absolute;
  top: -25px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 11px;
  font-weight: 600;
  color: #333;
  white-space: nowrap;
}

.chart-axis {
  position: absolute;
  bottom: -30px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
}

.axis-label {
  font-size: 12px;
  color: #666;
}

.color-distribution {
  margin-top: 20px;
}

.color-distribution h5 {
  color: #2d5a27;
  font-size: 16px;
  margin-bottom: 15px;
}

.color-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.color-bar {
  display: flex;
  align-items: center;
  gap: 10px;
}

.color-indicator {
  height: 20px;
  border-radius: 4px;
  min-width: 20px;
  transition: width 0.3s;
}

.color-indicator.green { background: #4CAF50; }
.color-indicator.yellow { background: #FFC107; }
.color-indicator.brown { background: #8D6E63; }
.color-indicator.red { background: #F44336; }
.color-indicator.purple { background: #9C27B0; }
.color-indicator.variegated { background: linear-gradient(to right, #4CAF50, #FFC107, #F44336); }

.color-label {
  font-size: 14px;
  color: #333;
}

.growth-summary {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

.summary-item .label {
  font-weight: 500;
  color: #666;
}

.summary-item .value {
  font-weight: 600;
  color: #2d5a27;
}
</style>