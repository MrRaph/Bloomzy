<template>
  <nav class="app-navigation">
    <div class="nav-container">
      <!-- Logo -->
      <router-link to="/" class="nav-logo">
        <span class="logo-icon">🌱</span>
        <span class="logo-text">Bloomzy</span>
      </router-link>

      <!-- Navigation principale -->
      <div class="nav-links" v-if="authStore.isAuthenticated">
        <router-link to="/dashboard" class="nav-link">
          <span class="nav-icon">🏠</span>
          Dashboard
        </router-link>
        <router-link to="/my-plants" class="nav-link">
          <span class="nav-icon">🪴</span>
          Mes Plantes
        </router-link>
        <router-link to="/indoor-plants" class="nav-link">
          <span class="nav-icon">📚</span>
          Catalogue
        </router-link>
        <div class="nav-dropdown" @mouseenter="showDropdown = true" @mouseleave="showDropdown = false">
          <button class="nav-link dropdown-trigger">
            <span class="nav-icon">⚙️</span>
            Plus
            <span class="dropdown-arrow">▼</span>
          </button>
          <div class="dropdown-menu" v-show="showDropdown">
            <router-link to="/journal" class="dropdown-item">
              <span class="nav-icon">📖</span>
              Journal
            </router-link>
            <router-link to="/community" class="dropdown-item">
              <span class="nav-icon">👥</span>
              Communauté
            </router-link>
            <router-link to="/settings" class="dropdown-item">
              <span class="nav-icon">⚙️</span>
              Paramètres
            </router-link>
          </div>
        </div>
      </div>

      <!-- Actions utilisateur -->
      <div class="nav-actions">
        <div v-if="authStore.isAuthenticated" class="user-menu">
          <div class="user-dropdown" @mouseenter="showUserMenu = true" @mouseleave="showUserMenu = false">
            <button class="user-button">
              <div class="user-avatar">
                <img 
                  v-if="authStore.user?.avatar_url" 
                  :src="authStore.user.avatar_url" 
                  :alt="authStore.user.username"
                />
                <span v-else class="avatar-placeholder">
                  {{ (authStore.user?.username || authStore.user?.email || '?')[0].toUpperCase() }}
                </span>
              </div>
              <span class="user-name">{{ authStore.user?.username || authStore.user?.email }}</span>
              <span class="dropdown-arrow">▼</span>
            </button>
            <div class="dropdown-menu user-dropdown-menu" v-show="showUserMenu">
              <router-link to="/profile" class="dropdown-item">
                <span class="nav-icon">👤</span>
                Mon Profil
              </router-link>
              <div class="dropdown-divider"></div>
              <button @click="logout" class="dropdown-item logout-btn">
                <span class="nav-icon">🚪</span>
                Déconnexion
              </button>
            </div>
          </div>
        </div>
        <div v-else class="auth-buttons">
          <router-link to="/login" class="btn btn-outline">Connexion</router-link>
          <router-link to="/signup" class="btn btn-primary">Inscription</router-link>
        </div>
      </div>

      <!-- Menu mobile -->
      <button 
        class="mobile-menu-btn"
        @click="showMobileMenu = !showMobileMenu"
        v-if="authStore.isAuthenticated"
      >
        ☰
      </button>
    </div>

    <!-- Menu mobile overlay -->
    <div class="mobile-menu" v-if="showMobileMenu" @click="showMobileMenu = false">
      <div class="mobile-menu-content" @click.stop>
        <div class="mobile-menu-header">
          <span class="logo-icon">🌱</span>
          <span class="logo-text">Bloomzy</span>
          <button @click="showMobileMenu = false" class="close-btn">&times;</button>
        </div>
        <div class="mobile-nav-links">
          <router-link to="/dashboard" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">🏠</span>
            Dashboard
          </router-link>
          <router-link to="/my-plants" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">🪴</span>
            Mes Plantes
          </router-link>
          <router-link to="/indoor-plants" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">📚</span>
            Catalogue
          </router-link>
          <router-link to="/journal" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">📖</span>
            Journal
          </router-link>
          <router-link to="/community" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">👥</span>
            Communauté
          </router-link>
          <router-link to="/profile" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">👤</span>
            Mon Profil
          </router-link>
          <router-link to="/settings" @click="showMobileMenu = false" class="mobile-nav-link">
            <span class="nav-icon">⚙️</span>
            Paramètres
          </router-link>
          <button @click="logout" class="mobile-nav-link logout-btn">
            <span class="nav-icon">🚪</span>
            Déconnexion
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const showDropdown = ref(false)
const showUserMenu = ref(false)
const showMobileMenu = ref(false)

const logout = async () => {
  await authStore.logout()
  showUserMenu.value = false
  showMobileMenu.value = false
  router.push('/')
}
</script>

<style scoped>
.app-navigation {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
}

.nav-logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  color: #2d3748;
  font-weight: 700;
  font-size: 1.25rem;
}

.logo-icon {
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  text-decoration: none;
  color: #4a5568;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.nav-link:hover {
  background: #f7fafc;
  color: #2d3748;
}

.nav-link.router-link-active {
  background: #ebf8ff;
  color: #3182ce;
}

.nav-icon {
  font-size: 1rem;
}

.nav-dropdown {
  position: relative;
}

.dropdown-trigger {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.dropdown-arrow {
  font-size: 0.75rem;
  transition: transform 0.2s;
}

.nav-dropdown:hover .dropdown-arrow {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  min-width: 180px;
  z-index: 1000;
  padding: 0.5rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  text-decoration: none;
  color: #4a5568;
  transition: background-color 0.2s;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
}

.dropdown-item:hover {
  background: #f7fafc;
}

.dropdown-divider {
  height: 1px;
  background: #e2e8f0;
  margin: 0.5rem 0;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-dropdown {
  position: relative;
}

.user-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.user-button:hover {
  background: #f7fafc;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  background: #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  font-weight: 600;
  color: #4a5568;
}

.user-name {
  color: #2d3748;
  font-weight: 500;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-dropdown-menu {
  right: 0;
  left: auto;
}

.auth-buttons {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  cursor: pointer;
  border: 1px solid transparent;
}

.btn-outline {
  color: #4a5568;
  border-color: #e2e8f0;
}

.btn-outline:hover {
  background: #f7fafc;
}

.btn-primary {
  background: #4299e1;
  color: white;
}

.btn-primary:hover {
  background: #3182ce;
}

.mobile-menu-btn {
  display: none;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #4a5568;
}

.mobile-menu {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.mobile-menu-content {
  background: white;
  width: 80%;
  max-width: 300px;
  height: 100%;
  overflow-y: auto;
}

.mobile-menu-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  border-bottom: 1px solid #e2e8f0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #a0aec0;
}

.mobile-nav-links {
  padding: 1rem 0;
}

.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  text-decoration: none;
  color: #4a5568;
  transition: background-color 0.2s;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-size: 1rem;
}

.mobile-nav-link:hover {
  background: #f7fafc;
}

.mobile-nav-link.router-link-active {
  background: #ebf8ff;
  color: #3182ce;
}

.logout-btn {
  color: #e53e3e;
}

.logout-btn:hover {
  background: #fed7d7;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .mobile-menu-btn {
    display: block;
  }

  .mobile-menu {
    display: block;
  }

  .user-name {
    display: none;
  }

  .auth-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }

  .btn {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .nav-container {
    padding: 0 0.5rem;
  }

  .logo-text {
    display: none;
  }
}
</style>
