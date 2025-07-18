<template>
  <div id="app">
    <template v-if="!authStore.isAuthReady">
      <div class="loading-overlay">
        <div class="spinner"></div>
        <div class="loading-text">Chargement...</div>
      </div>
    </template>
    <template v-else>
      <AppNavigation />
      <main class="main-content">
        <router-view />
      </main>
      <NotificationSystem ref="notificationRef" />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotifications } from '@/composables/useNotifications'
import AppNavigation from '@/components/AppNavigation.vue'
import NotificationSystem from '@/components/NotificationSystem.vue'

const authStore = useAuthStore()
const { setNotificationInstance } = useNotifications()
const notificationRef = ref()

onMounted(() => {
  if (notificationRef.value) {
    setNotificationInstance(notificationRef.value)
  }
})
</script>

<style>
/* Overlay de chargement global */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255,255,255,0.85);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.spinner {
  border: 6px solid #e5e7eb;
  border-top: 6px solid #059669;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.loading-text {
  color: #059669;
  font-size: 1.2rem;
  font-weight: 500;
}
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: #f8fafc;
  color: #334155;
}

.navbar {
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav-brand .brand-link {
  text-decoration: none;
  color: #059669;
}

.nav-brand h1 {
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-link {
  text-decoration: none;
  color: #64748b;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  transition: all 0.2s;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
}

.nav-link:hover {
  color: #059669;
  background-color: #f0fdf4;
}

.btn-primary {
  background-color: #059669 !important;
  color: white !important;
}

.btn-primary:hover {
  background-color: #047857 !important;
}

.btn-logout {
  color: #dc2626 !important;
}

.btn-logout:hover {
  background-color: #fef2f2 !important;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>