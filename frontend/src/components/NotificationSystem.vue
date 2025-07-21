<template>
  <Teleport to="body">
    <div class="notification-container">
      <TransitionGroup name="notification" tag="div">
        <div
          v-for="notification in notifications"
          :key="notification.id"
          class="notification"
          :class="`notification--${notification.type}`"
          @click="removeNotification(notification.id)"
        >
          <div class="notification-icon">
            {{ getIcon(notification.type) }}
          </div>
          <div class="notification-content">
            <div class="notification-title" v-if="notification.title">
              {{ notification.title }}
            </div>
            <div class="notification-message">
              {{ notification.message }}
            </div>
          </div>
          <button 
            class="notification-close"
            @click.stop="removeNotification(notification.id)"
            aria-label="Fermer la notification"
          >
            ×
          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import type { Notification } from '@/types'

const notifications = ref<Notification[]>([])
const timeouts = new Map<string, number>()

const getIcon = (type: string) => {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️'
  }
  return icons[type as keyof typeof icons] || 'ℹ️'
}

const addNotification = (notification: Omit<Notification, 'id'>) => {
  const id = Date.now().toString() + Math.random().toString(36).substr(2, 9)
  const newNotification: Notification = {
    id,
    duration: 5000,
    ...notification
  }

  notifications.value.push(newNotification)

  // Auto-remove après la durée spécifiée (sauf si persistent)
  if (!newNotification.persistent && newNotification.duration) {
    const timeout = window.setTimeout(() => {
      removeNotification(id)
    }, newNotification.duration)
    timeouts.set(id, timeout)
  }

  return id
}

const removeNotification = (id: string) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }

  // Clear timeout si il existe
  const timeout = timeouts.get(id)
  if (timeout) {
    clearTimeout(timeout)
    timeouts.delete(id)
  }
}

const clearAll = () => {
  notifications.value = []
  timeouts.forEach(timeout => clearTimeout(timeout))
  timeouts.clear()
}

// Méthodes de convenance
const success = (message: string, title?: string, options?: Partial<Notification>) => {
  return addNotification({ type: 'success', message, title, ...options })
}

const error = (message: string, title?: string, options?: Partial<Notification>) => {
  return addNotification({ type: 'error', message, title, ...options })
}

const warning = (message: string, title?: string, options?: Partial<Notification>) => {
  return addNotification({ type: 'warning', message, title, ...options })
}

const info = (message: string, title?: string, options?: Partial<Notification>) => {
  return addNotification({ type: 'info', message, title, ...options })
}

// Nettoyage lors du démontage
onUnmounted(() => {
  timeouts.forEach(timeout => clearTimeout(timeout))
})

// Exposition des méthodes
defineExpose({
  addNotification,
  removeNotification,
  clearAll,
  success,
  error,
  warning,
  info
})
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 80px;
  right: 1rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  pointer-events: none;
}

.notification {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  min-width: 320px;
  max-width: 400px;
  padding: 1rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border-left: 4px solid;
  cursor: pointer;
  pointer-events: auto;
  transition: all 0.3s ease;
}

.notification:hover {
  transform: translateX(-4px);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
}

.notification--success {
  border-left-color: #10b981;
  background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
}

.notification--error {
  border-left-color: #ef4444;
  background: linear-gradient(135deg, #fef2f2 0%, #fef2f2 100%);
}

.notification--warning {
  border-left-color: #f59e0b;
  background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%);
}

.notification--info {
  border-left-color: #3b82f6;
  background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%);
}

.notification-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
  margin-top: 0.125rem;
}

.notification-content {
  flex: 1;
  min-width: 0;
}

.notification-title {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
}

.notification-message {
  color: #4b5563;
  font-size: 0.875rem;
  line-height: 1.4;
  word-wrap: break-word;
}

.notification-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #9ca3af;
  cursor: pointer;
  transition: color 0.2s;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.notification-close:hover {
  color: #6b7280;
}

/* Animations */
.notification-enter-active {
  transition: all 0.4s ease;
}

.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}

/* Responsive */
@media (max-width: 640px) {
  .notification-container {
    top: 70px;
    right: 0.5rem;
    left: 0.5rem;
  }

  .notification {
    min-width: auto;
    max-width: none;
    margin: 0;
  }

  .notification-enter-from,
  .notification-leave-to {
    transform: translateY(-100%);
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .notification {
    background: #1f2937;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  }

  .notification--success {
    background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
  }

  .notification--error {
    background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
  }

  .notification--warning {
    background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
  }

  .notification--info {
    background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
  }

  .notification-title {
    color: #f9fafb;
  }

  .notification-message {
    color: #d1d5db;
  }

  .notification-close {
    color: #9ca3af;
  }

  .notification-close:hover {
    color: #d1d5db;
  }
}
</style>
