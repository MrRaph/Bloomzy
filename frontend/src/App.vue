<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <router-link to="/" class="brand-link">
          <h1>🌱 Bloomzy</h1>
        </router-link>
      </div>
      <div class="nav-links">
        <template v-if="!authStore.isAuthenticated">
          <router-link to="/login" class="nav-link">Connexion</router-link>
          <router-link to="/signup" class="nav-link btn-primary">Inscription</router-link>
        </template>
        <template v-else>
          <router-link to="/profile" class="nav-link">Mon profil</router-link>
          <button @click="logout" class="nav-link btn-logout">Déconnexion</button>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
}
</script>

<style>
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