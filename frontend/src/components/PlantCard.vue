<template>
  <div class="plant-card" :class="{ 'plant-card--compact': compact }">
    <!-- Photo de la plante -->
    <div class="plant-photo">
      <img 
        v-if="plant.current_photo_url" 
        :src="plant.current_photo_url" 
        :alt="plant.custom_name"
        class="plant-image"
        @error="handleImageError"
      />
      <div v-else class="plant-placeholder">
        <span class="placeholder-icon">🌿</span>
        <span v-if="!compact" class="placeholder-text">Aucune photo</span>
      </div>
      
      <!-- Badge de statut -->
      <div class="status-badge" :class="`status-${plant.health_status}`">
        {{ getStatusIcon(plant.health_status) }}
      </div>
    </div>
    
    <!-- Informations de la plante -->
    <div class="plant-info">
      <h3 class="plant-name">{{ plant.custom_name }}</h3>
      
      <p v-if="plant.species && !compact" class="plant-species">
        {{ plant.species.scientific_name }}
      </p>
      
      <div class="plant-meta">
        <span v-if="plant.location" class="meta-item">
          📍 {{ plant.location }}
        </span>
        <span v-if="plant.pot_size && !compact" class="meta-item">
          🪴 {{ plant.pot_size }}
        </span>
      </div>

      <!-- Informations d'arrosage (si disponibles) -->
      <div v-if="wateringInfo && !compact" class="watering-info">
        <div class="watering-status" :class="wateringInfo.status">
          <span class="watering-icon">{{ getWateringIcon(wateringInfo.status) }}</span>
          <span class="watering-text">{{ wateringInfo.message }}</span>
        </div>
        <div v-if="wateringInfo.lastWatering" class="last-watering">
          Dernier arrosage: {{ formatDate(wateringInfo.lastWatering) }}
        </div>
      </div>

      <!-- Actions de la carte -->
      <div class="plant-actions" v-if="showActions">
        <button 
          v-if="actions.includes('water')"
          @click="$emit('water', plant)" 
          class="action-btn action-btn--primary"
          :title="'Arroser ' + plant.custom_name"
        >
          💧
        </button>
        <button 
          v-if="actions.includes('photo')"
          @click="$emit('photo', plant)" 
          class="action-btn action-btn--secondary"
          :title="'Photo de ' + plant.custom_name"
        >
          📷
        </button>
        <button 
          v-if="actions.includes('edit')"
          @click="$emit('edit', plant)" 
          class="action-btn action-btn--secondary"
          :title="'Modifier ' + plant.custom_name"
        >
          ✏️
        </button>
        <button 
          v-if="actions.includes('details')"
          @click="$emit('details', plant)" 
          class="action-btn action-btn--secondary"
          :title="'Détails de ' + plant.custom_name"
        >
          👁️
        </button>
        <button 
          v-if="actions.includes('delete')"
          @click="$emit('delete', plant)" 
          class="action-btn action-btn--danger"
          :title="'Supprimer ' + plant.custom_name"
        >
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { UserPlant } from '@/types'

interface WateringInfo {
  status: 'overdue' | 'due' | 'upcoming' | 'recent'
  message: string
  lastWatering?: string
  nextWatering?: string
}

interface Props {
  plant: UserPlant
  compact?: boolean
  showActions?: boolean
  actions?: Array<'water' | 'photo' | 'edit' | 'details' | 'delete'>
  wateringInfo?: WateringInfo | null
}

const props = withDefaults(defineProps<Props>(), {
  compact: false,
  showActions: true,
  actions: () => ['water', 'edit', 'details', 'delete']
})

const emit = defineEmits<{
  water: [plant: UserPlant]
  photo: [plant: UserPlant]
  edit: [plant: UserPlant]
  details: [plant: UserPlant]
  delete: [plant: UserPlant]
}>()

const getStatusIcon = (status: string) => {
  const icons = {
    healthy: '💚',
    sick: '😷',
    dying: '💔',
    dead: '💀'
  }
  return icons[status as keyof typeof icons] || '❓'
}

const getWateringIcon = (status: string) => {
  const icons = {
    overdue: '🚨',
    due: '💧',
    upcoming: '⏰',
    recent: '✅'
  }
  return icons[status as keyof typeof icons] || '💧'
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) {
    return "Aujourd'hui"
  } else if (diffDays === 1) {
    return "Hier"
  } else if (diffDays < 7) {
    return `Il y a ${diffDays} jours`
  } else {
    return date.toLocaleDateString('fr-FR', { 
      day: 'numeric', 
      month: 'short' 
    })
  }
}

const handleImageError = (event: Event) => {
  // Cache l'image en cas d'erreur de chargement
  const img = event.target as HTMLImageElement
  img.style.display = 'none'
}
</script>

<style scoped>
.plant-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #f1f5f9;
}

.plant-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.plant-card--compact {
  max-width: 200px;
}

.plant-photo {
  position: relative;
  height: 180px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.plant-card--compact .plant-photo {
  height: 120px;
}

.plant-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.plant-card:hover .plant-image {
  transform: scale(1.05);
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

.plant-card--compact .placeholder-icon {
  font-size: 2rem;
  margin-bottom: 0;
}

.placeholder-text {
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  font-weight: 600;
  backdrop-filter: blur(8px);
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.status-healthy {
  background: rgba(34, 197, 94, 0.9);
}

.status-sick {
  background: rgba(239, 68, 68, 0.9);
}

.status-dying {
  background: rgba(245, 158, 11, 0.9);
}

.status-dead {
  background: rgba(107, 114, 128, 0.9);
}

.plant-info {
  padding: 1.5rem;
}

.plant-card--compact .plant-info {
  padding: 1rem;
}

.plant-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
}

.plant-card--compact .plant-name {
  font-size: 1rem;
  margin-bottom: 0.25rem;
}

.plant-species {
  margin: 0 0 0.75rem 0;
  font-size: 0.875rem;
  color: #64748b;
  font-style: italic;
  line-height: 1.4;
}

.plant-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.plant-card--compact .plant-meta {
  margin-bottom: 0.5rem;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  font-size: 0.75rem;
  color: #64748b;
  background: #f8fafc;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  font-weight: 500;
}

.watering-info {
  margin-bottom: 1rem;
  padding: 0.75rem;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 3px solid transparent;
}

.watering-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.watering-status.overdue {
  color: #dc2626;
}

.watering-status.overdue + .watering-info {
  border-left-color: #dc2626;
}

.watering-status.due {
  color: #2563eb;
}

.watering-status.due + .watering-info {
  border-left-color: #2563eb;
}

.watering-status.upcoming {
  color: #059669;
}

.watering-status.upcoming + .watering-info {
  border-left-color: #059669;
}

.watering-status.recent {
  color: #16a34a;
}

.watering-status.recent + .watering-info {
  border-left-color: #16a34a;
}

.watering-text {
  font-size: 0.875rem;
  font-weight: 500;
}

.last-watering {
  font-size: 0.75rem;
  color: #64748b;
}

.plant-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f1f5f9;
  color: #475569;
}

.action-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.action-btn--primary {
  background: #3b82f6;
  color: white;
}

.action-btn--primary:hover {
  background: #2563eb;
}

.action-btn--secondary {
  background: #6b7280;
  color: white;
}

.action-btn--secondary:hover {
  background: #4b5563;
}

.action-btn--danger {
  background: #ef4444;
  color: white;
}

.action-btn--danger:hover {
  background: #dc2626;
}

/* Responsive */
@media (max-width: 640px) {
  .plant-card {
    max-width: none;
  }
  
  .plant-photo {
    height: 150px;
  }
  
  .plant-info {
    padding: 1rem;
  }
  
  .action-btn {
    width: 32px;
    height: 32px;
    font-size: 0.875rem;
  }
}
</style>
