<template>
  <div class="dashboard-page">
    <h1>Bienvenue sur votre dashboard, {{ authStore.user?.username || authStore.user?.email }} !</h1>
    <p>Accédez rapidement à toutes les fonctionnalités de Bloomzy :</p>
    <div class="dashboard-menu">
      <router-link to="/profile" class="dashboard-btn">Mon profil</router-link>
      <router-link to="/plants" class="dashboard-btn">Mes plantes</router-link>
      <router-link to="/journal" class="dashboard-btn">Journal de croissance</router-link>
      <router-link to="/community" class="dashboard-btn">Communauté</router-link>
      <router-link to="/settings" class="dashboard-btn">Paramètres</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>

<style scoped>
.dashboard-page {
  padding: 2rem;
  max-width: 700px;
  margin: 0 auto;
}
.dashboard-menu {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-top: 2rem;
}
.dashboard-btn {
  background: #059669;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.2s;
}
.dashboard-btn:hover {
  background: #047857;
}
</style>
