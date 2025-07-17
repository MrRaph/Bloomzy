<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          🌱 Bloomzy
        </h1>
        <p class="hero-subtitle">
          Votre assistant intelligent pour la gestion de vos plantes d'intérieur et jardin
        </p>
        <div class="hero-buttons" v-if="!authStore.isAuthenticated">
          <router-link to="/signup" class="btn btn-primary">
            Commencer maintenant
          </router-link>
          <router-link to="/login" class="btn btn-secondary">
            Se connecter
          </router-link>
        </div>
        <div class="hero-welcome" v-else>
          <h2>Bienvenue, {{ authStore.user?.username || authStore.user?.email }}!</h2>
          <p>Prêt à prendre soin de vos plantes ?</p>
        </div>
      </div>
    </div>

    <div class="features-section">
      <div class="container">
        <h2 class="section-title">Fonctionnalités principales</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">🪴</div>
            <h3>Gestion des plantes</h3>
            <p>Suivez vos plantes d'intérieur et de jardin avec un catalogue complet d'espèces</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💧</div>
            <h3>Arrosage intelligent</h3>
            <p>Recevez des notifications personnalisées basées sur les besoins de vos plantes</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3>Journal de croissance</h3>
            <p>Documentez l'évolution de vos plantes avec photos et métriques</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <h3>Assistant IA</h3>
            <p>Obtenez des conseils personnalisés grâce à l'intelligence artificielle</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">👥</div>
            <h3>Communauté</h3>
            <p>Partagez vos expériences et apprenez des autres jardiniers</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🌦️</div>
            <h3>Météo intégrée</h3>
            <p>Adaptation automatique aux conditions météorologiques locales</p>
          </div>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <div class="container">
        <h2>Rejoignez la communauté Bloomzy</h2>
        <p>Commencez votre voyage vers un jardinage plus intelligent dès aujourd'hui</p>
        <router-link to="/signup" class="btn btn-primary" v-if="!authStore.isAuthenticated">
          Créer un compte gratuit
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(() => {
  authStore.initializeAuth()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.hero-section {
  background: linear-gradient(135deg, #059669 0%, #065f46 100%);
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.hero-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.hero-welcome {
  padding: 2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  backdrop-filter: blur(10px);
}

.hero-welcome h2 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.btn-primary {
  background: white;
  color: #059669;
}

.btn-primary:hover {
  background: #f9fafb;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-secondary {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary:hover {
  background: white;
  color: #059669;
}

.features-section {
  padding: 4rem 2rem;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 2.5rem;
  text-align: center;
  margin-bottom: 3rem;
  color: #1f2937;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: #f8fafc;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  transition: transform 0.2s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #1f2937;
}

.feature-card p {
  color: #6b7280;
  line-height: 1.6;
}

.cta-section {
  background: #f0fdf4;
  padding: 4rem 2rem;
  text-align: center;
}

.cta-section h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #1f2937;
}

.cta-section p {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  color: #6b7280;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>