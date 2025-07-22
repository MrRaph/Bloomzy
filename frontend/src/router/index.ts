import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Signup from '@/views/Signup.vue'
import Profile from '@/views/Profile.vue'
import Dashboard from '@/views/Dashboard.vue'
import IndoorPlants from '@/views/IndoorPlants.vue'
import MyPlants from '@/views/MyPlants.vue'
import ApiKeys from '@/views/ApiKeys.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/login',
      name: 'login',
      component: Login,
      meta: { requiresGuest: true }
    },
    {
      path: '/signup',
      name: 'signup',
      component: Signup,
      meta: { requiresGuest: true }
    },
    {
      path: '/profile',
      name: 'profile',
      component: Profile,
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { requiresAuth: true }
    },
    {
      path: '/indoor-plants',
      name: 'indoor-plants',
      component: IndoorPlants,
      meta: { requiresAuth: true }
    },
    {
      path: '/my-plants',
      name: 'my-plants',
      component: MyPlants,
      meta: { requiresAuth: true }
    },
    {
      path: '/api-keys',
      name: 'api-keys',
      component: ApiKeys,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore()
  // Attendre que l'auth soit hydratée avant de vérifier
  if (!authStore.isAuthReady) {
    // On attend que isAuthReady passe à true (hydratation terminée)
    await new Promise(resolve => {
      const stop = authStore.$subscribe(() => {
        if (authStore.isAuthReady) {
          stop()
          resolve(true)
        }
      })
    })
  }
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router